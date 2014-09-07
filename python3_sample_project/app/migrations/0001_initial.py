# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'Categories',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericNote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('title', models.CharField(max_length=50)),
                ('object_id', models.PositiveIntegerField(verbose_name='Content id')),
                ('content_type', models.ForeignKey(related_name='generic_notes', verbose_name='Content type', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('text', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_board_member', models.BooleanField(verbose_name='Board Member', default=False)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'People',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('category', adminsortable.fields.SortableForeignKey(to='app.Category')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='note',
            name='project',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='credit',
            name='project',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='component',
            name='widget',
            field=adminsortable.fields.SortableForeignKey(to='app.Widget'),
            preserve_default=True,
        ),
    ]
