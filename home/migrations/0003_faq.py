# Generated by Django 3.0.6 on 2020-07-10 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200520_0344'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField()),
                ('question', models.CharField(max_length=200)),
                ('answer', models.TextField()),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]