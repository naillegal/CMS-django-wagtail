# Generated by Django 5.0.3 on 2024-04-04 09:06

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_formpage_formfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='blog.formpage'),
        ),
    ]
