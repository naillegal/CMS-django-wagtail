# Generated by Django 5.0.3 on 2024-04-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_postpage_header_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postpage',
            name='body',
        ),
        migrations.AddField(
            model_name='postpage',
            name='image_text_1',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
        migrations.AddField(
            model_name='postpage',
            name='image_text_2',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
        migrations.AddField(
            model_name='postpage',
            name='image_text_caption1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='postpage',
            name='image_text_caption2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='postpage',
            name='paragraph',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postpage',
            name='quotes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postpage',
            name='quotes_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
