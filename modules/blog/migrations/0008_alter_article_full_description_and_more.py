# Generated by Django 4.2.6 on 2023-11-01 07:37

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='full_description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='article',
            name='short_description',
            field=django_ckeditor_5.fields.CKEditor5Field(max_length=500, verbose_name='Краткое описание'),
        ),
    ]