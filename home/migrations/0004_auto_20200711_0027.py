# Generated by Django 3.0.6 on 2020-07-10 23:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]