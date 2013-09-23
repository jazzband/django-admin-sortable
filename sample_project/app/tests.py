import httplib
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client, RequestFactory

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable
from adminsortable.utils import get_is_sortable
from app.models import Category, Credit, Note


class BadSortableModel(models.Model):
    note = SortableForeignKey(Note)
    credit = SortableForeignKey(Credit)


class TestSortableModel(Sortable):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class SortableTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user_raw_password = 'admin'
        self.user = User.objects.create_user('admin', 'admin@admin.com',
            self.user_raw_password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def create_category(self, title='Category 1'):
        category = Category.objects.create(title=title)
        return category

    def test_new_user_is_authenticated(self):
        self.assertEqual(self.user.is_authenticated(), True,
            'User is not authenticated')

    def test_new_user_is_staff(self):
        self.assertEqual(self.user.is_staff, True, 'User is not staff')

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

    def test_save_order_incremented(self):
        category1 = self.create_category()
        self.assertEqual(category1.order, 1, 'Category 1 order should be 1.')

        category2 = self.create_category(title='Category 2')
        self.assertEqual(category2.order, 2, 'Category 2 order should be 2.')

    def test_adminsortable_change_list_view(self):
        self.client.login(username=self.user.username,
            password=self.user_raw_password)
        response = self.client.get('/admin/app/category/sort/')
        self.assertEquals(response.status_code, httplib.OK,
            'Unable to reach sort view.')

    def make_test_categories(self):
        category1 = self.create_category()
        category2 = self.create_category(title='Category 2')
        category3 = self.create_category(title='Category 3')
        return category1, category2, category3

    def get_sorting_url(self):
        return '/admin/app/category/sorting/do-sorting/{0}/'.format(
            Category.model_type_id())

    def get_category_indexes(self, *categories):
        return {'indexes': ','.join([str(c.id) for c in categories])}

    def test_adminsortable_changelist_templates(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        response = self.client.get('/admin/app/category/sort/')
        self.assertEqual(response.status_code, httplib.OK,
            'Admin sort request failed.')

        #assert adminsortable change list templates are used
        template_names = [t.name for t in response.templates]
        self.assertTrue('adminsortable/change_list.html' in template_names,
                        'adminsortable/change_list.html was not rendered')

    def test_adminsortable_change_list_sorting_fails_if_not_ajax(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        category1, category2, category3 = self.make_test_categories()
        #make a normal POST
        response = self.client.post(self.get_sorting_url(),
            data=self.get_category_indexes(category1, category2, category3))
        content = json.loads(response.content)
        self.assertFalse(content.get('objects_sorted'),
            'Objects should not have been sorted. An ajax post is required.')

    def test_adminsortable_change_list_sorting_successful(self):
        logged_in = self.client.login(username=self.user.username,
            password=self.user_raw_password)
        self.assertTrue(logged_in, 'User is not logged in')

        #make categories
        category1, category2, category3 = self.make_test_categories()

        #make an Ajax POST
        response = self.client.post(self.get_sorting_url(),
            data=self.get_category_indexes(category3, category2, category1),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertTrue(content.get('objects_sorted'),
            'Objects should have been sorted.')

        #assert order is correct
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
