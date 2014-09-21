# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonSortableCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Non-Sortable Category',
                'verbose_name_plural': 'Non-Sortable Categories',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SortableCategoryWidget',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, default=1)),
                ('title', models.CharField(max_length=50)),
                ('non_sortable_category', adminsortable.fields.SortableForeignKey(to='app.NonSortableCategory')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Sortable Category Widget',
                'abstract': False,
                'verbose_name_plural': 'Sortable Category Widgets',
            },
            bases=(models.Model,),
        ),
    ]
