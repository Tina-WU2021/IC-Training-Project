# Generated by Django 3.2.6 on 2022-07-14 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0004_auto_20220714_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created'),
        ),
    ]