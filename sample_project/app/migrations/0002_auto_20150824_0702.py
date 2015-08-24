# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomWidgetComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('widget_order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
            ],
            options={
                'ordering': ['widget_order'],
                'verbose_name': 'Custom Widget Component',
                'verbose_name_plural': 'Custom Widget Components',
            },
        ),
        migrations.AlterField(
            model_name='customwidget',
            name='custom_order_field',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='customwidgetcomponent',
            name='custom_widget',
            field=models.ForeignKey(to='app.CustomWidget'),
        ),
    ]
