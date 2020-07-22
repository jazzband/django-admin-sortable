try:
    import httplib  # Python 2
except ImportError:
    import http.client as httplib  # Python 3

import json

import django

from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.test.client import Client

from adminsortable.models import SortableMixin
from adminsortable.utils import get_is_sortable
from .models import Category, Person, Project, TestNonAutoFieldModel


class SortableTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_raw_password = 'admin'
        self.user = User.objects.create_user('admin', 'admin@admin.com',
                                             self.user_raw_password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.staff_raw_password = 'staff'
        self.staff = User.objects.create_user('staff', 'staff@staff.com',
                                              self.staff_raw_password)
        self.staff.is_staff = True
        self.user.is_superuser = False
        self.staff.save()

        # create people
        Person.objects.create(first_name='Bob', last_name='Smith',
            is_board_member=True)
        Person.objects.create(first_name='Sally', last_name='Sue',
            is_board_member=False)
        Person.objects.create(first_name='Mike', last_name='Wilson',
            is_board_member=True)
        Person.objects.create(first_name='Robert', last_name='Roberts',
            is_board_member=True)

        self.people = Person.objects.all()
        self.first_person = self.people[0]
        self.second_person = self.people[1]
        self.third_person = self.people[2]
        self.fourth_person = self.people[3]

    def create_category(self, title='Category 1'):
        category = Category.objects.create(title=title)
        return category

    def test_new_user_is_authenticated(self):
        if django.VERSION < (1, 10):
            self.assertEqual(self.user.is_authenticated(), True,
                'User is not authenticated')
        else:
            self.assertEqual(self.user.is_authenticated, True,
                'User is not authenticated')

    def test_new_user_is_staff(self):
        self.assertEqual(self.user.is_staff, True, 'User is not staff')

    def test_new_staff_is_staff(self):
        self.assertEqual(self.staff.is_staff, True, 'Staff User is not staff')

    def test_is_not_sortable(self):
        """
        A model should only become sortable if it has more than
        record to sort.
        """
        self.create_category()
        self.assertFalse(get_is_sortable(Category.objects.all()),
            'Category only has one record. It should not be sortable.')

    def test_is_sortable(self):
        self.create_category()
        self.create_category(title='Category 2')
        self.assertTrue(get_is_sortable(Category.objects.all()),
            'Category has more than one record. It should be sortable.')

    def test_doesnt_overwrite_preexisting_order_field_value(self):
        self.create_category()
        category = Category.objects.create(title='Category 2', order=5)
        self.assertEqual(category.order, 5)

    def test_save_order_incremented(self):
        category1 = self.create_category()
        self.assertEqual(category1.order, 1, 'Category 1 order should be 1.')

        category2 = self.create_category(title='Category 2')
        self.assertEqual(category2.order, 2, 'Category 2 order should be 2.')

    def test_adminsortable_change_list_view(self):
        self.client.login(username=self.user.username,
            password=self.user_raw_password)
        response = self.client.get('/admin/samples/category/sort/')
        self.assertEqual(response.status_code, httplib.OK,
            'Unable to reach sort view.')

    def make_test_categories(self):
        category1 = self.create_category()
        category2 = self.create_category(title='Category 2')
        category3 = self.create_category(title='Category 3')
        return category1, category2, category3

    def get_sorting_url(self, model):
        return '/admin/samples/project/sort/do-sorting/{0}/'.format(
            model.model_type_id())

    def get_category_indexes(self, *categories):
        return {'indexes': ','.join([str(c.id) for c in categories])}

    def test_adminsortable_changelist_templates(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        response = self.client.get('/admin/samples/category/sort/')
        self.assertEqual(response.status_code, httplib.OK,
            'Admin sort request failed.')

        # assert adminsortable change list templates are used
        template_names = [t.name for t in response.templates]
        self.assertTrue('adminsortable/change_list.html' in template_names,
                        'adminsortable/change_list.html was not rendered')

    def test_adminsortable_change_list_sorting_fails_if_not_post(self):
        logged_in = self.client.login(username=self.user.username,
                                      password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        category1, category2, category3 = self.make_test_categories()
        # make a normal GET
        response = self.client.get(
            self.get_sorting_url(Category),
            data=self.get_category_indexes(category1, category2, category3))

        self.assertEqual(
            response.status_code,
            httplib.METHOD_NOT_ALLOWED,
            'Objects should not have been sorted. A POST method is required.')

    def test_adminsortable_change_list_sorting_fails_permission_denied(self):
        logged_in = self.client.login(username=self.staff.username,
                                      password=self.staff_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        category1, category2, category3 = self.make_test_categories()
        # make a normal POST
        response = self.client.post(
            self.get_sorting_url(Category),
            data=self.get_category_indexes(category1, category2, category3))

        self.assertEqual(
            response.status_code,
            httplib.FORBIDDEN,
            'Objects should not have been sorted. User is not allowed.')

    def test_adminsortable_change_list_sorting_fails_if_not_ajax(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        category1, category2, category3 = self.make_test_categories()
        # make a normal POST
        response = self.client.post(self.get_sorting_url(Category),
            data=self.get_category_indexes(category1, category2, category3))
        content = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertFalse(content.get('objects_sorted'),
            'Objects should not have been sorted. An ajax post is required.')

    def test_adminsortable_change_list_sorting_successful(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        # make categories
        category1, category2, category3 = self.make_test_categories()

        # make an Ajax POST
        response = self.client.post(self.get_sorting_url(Category),
            data=self.get_category_indexes(category3, category2, category1),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertTrue(content.get('objects_sorted'),
            'Objects should have been sorted.')

        # assert order is correct
        categories = Category.objects.all()
        cat1 = categories[0]
        cat2 = categories[1]
        cat3 = categories[2]

        self.assertEqual(cat1.order, 1,
            'First category returned should have order == 1')
        self.assertEqual(cat1.pk, 3,
            'Category ID 3 should have been first in queryset')

        self.assertEqual(cat2.order, 2,
            'Second category returned should have order == 2')
        self.assertEqual(cat2.pk, 2,
            'Category ID 2 should have been second in queryset')

        self.assertEqual(cat3.order, 3,
            'Third category returned should have order == 3')
        self.assertEqual(cat3.pk, 1,
            'Category ID 1 should have been third in queryset')

    def test_get_next(self):
        for index, person in enumerate(self.people):
            next_index = index + 1
            next_person = self.people[index].get_next()

            if next_index < len(self.people):
                self.assertEqual(next_person, self.people[next_index],
                    'Next person should be "{0}"'.format(
                        self.people[next_index]))

    def test_get_previous(self):
        for person in self.people:
            previous_person = person.get_previous()

            # get_previous() returns `None` if there isn't a previous object
            if previous_person:
                self.assertEqual(previous_person,
                    self.people.get(order=person.order - 1),
                    'Previous person for "{0}" (order: {1}) should be "{2}"'
                    '(order: {3})'.format(person, person.order,
                        previous_person, previous_person.order))

    def test_adminsortable_change_list_view_loads_with_sortable_fk(self):
        category1 = self.create_category(title='Category 3')
        Project.objects.create(category=category1, description="foo")

        self.client.login(username=self.user.username,
            password=self.user_raw_password)
        response = self.client.get('/admin/samples/project/sort/')
        self.assertEqual(response.status_code, httplib.OK,
            'Unable to reach sort view.')

    def test_adminsortable_change_list_view_permission_denied(self):
        category1 = self.create_category(title='Category 3')
        Project.objects.create(category=category1, description="foo")

        self.client.login(username=self.staff.username,
                          password=self.staff_raw_password)
        response = self.client.get('/admin/samples/project/sort/')
        self.assertEqual(response.status_code, httplib.FORBIDDEN,
                         'Sort view must be forbidden.')

    def test_adminsortable_inline_changelist_success(self):
        self.client.login(username=self.user.username,
                          password=self.user_raw_password)

        project = Project.objects.create(
            category=self.create_category(),
            description='Test project'
        )
        note1 = project.note_set.create(text='note 1')
        note2 = project.note_set.create(text='note 2')
        note3 = project.note_set.create(text='note 3')

        response = self.client.post(
            self.get_sorting_url(project.note_set.model),
            data=self.get_category_indexes(note3, note2, note1),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(
            response.status_code,
            httplib.OK,
            'Note inline must be sortable in ProjectAdmin')
        content = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertTrue(content.get('objects_sorted'),
                        'Objects should have been sorted.')

        notes = list(project.note_set.all().values('id', 'order', 'text'))
        expected_notes = [
            {
                'id': note3.pk,
                'order': 1,
                'text': note3.text,
            },
            {
                'id': note2.pk,
                'order': 2,
                'text': note2.text,
            },
            {
                'id': note1.pk,
                'order': 3,
                'text': note1.text,
            }
        ]
        self.assertEqual(notes, expected_notes)

    def test_save_non_auto_field_model(self):
        model = TestNonAutoFieldModel()
        model.save()
