# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='GenericNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('object_id', models.PositiveIntegerField(verbose_name='Content id')),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
                ('content_type', models.ForeignKey(related_name='generic_notes', verbose_name='Content type', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='NonSortableCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Non-Sortable Category',
                'verbose_name_plural': 'Non-Sortable Categories',
            },
        ),
        migrations.CreateModel(
            name='NonSortableCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='NonSortableNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_board_member', models.BooleanField(default=False, verbose_name=b'Board Member')),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
                ('category', adminsortable.fields.SortableForeignKey(to='app.Category')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SortableCategoryWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
                ('non_sortable_category', adminsortable.fields.SortableForeignKey(to='app.NonSortableCategory')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Sortable Category Widget',
                'verbose_name_plural': 'Sortable Category Widgets',
            },
        ),
        migrations.CreateModel(
            name='SortableNonInlineCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
                ('non_sortable_category', adminsortable.fields.SortableForeignKey(to='app.NonSortableCategory')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Sortable Non-Inline Category',
                'verbose_name_plural': 'Sortable Non-Inline Categories',
            },
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CustomWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('custom_order_field', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['custom_order_field'], 'verbose_name': 'Custom Widget', 'verbose_name_plural': 'Custom Widgets'
            },
        ),
        migrations.AddField(
            model_name='note',
            name='project',
            field=models.ForeignKey(to='app.Project'),
        ),
        migrations.AddField(
            model_name='nonsortablenote',
            name='project',
            field=models.ForeignKey(to='app.Project'),
        ),
        migrations.AddField(
            model_name='nonsortablecredit',
            name='project',
            field=models.ForeignKey(to='app.Project'),
        ),
        migrations.AddField(
            model_name='credit',
            name='project',
            field=models.ForeignKey(to='app.Project'),
        ),
        migrations.AddField(
            model_name='component',
            name='widget',
            field=adminsortable.fields.SortableForeignKey(to='app.Widget'),
        ),
    ]
