# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_selfreferentialcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='selfreferentialcategory',
            options={'verbose_name_plural': 'Sortable Referential Categories', 'verbose_name': 'Sortable Referential Category'},
        ),
        migrations.AlterField(
            model_name='selfreferentialcategory',
            name='child',
            field=adminsortable.fields.SortableForeignKey(to='app.SelfReferentialCategory', null=True, blank=True),
        ),
    ]
