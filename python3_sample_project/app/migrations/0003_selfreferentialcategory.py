# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_nonsortablecategory_sortablecategorywidget'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfReferentialCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, default=1)),
                ('title', models.CharField(max_length=50)),
                ('child', adminsortable.fields.SortableForeignKey(to='app.SelfReferentialCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
