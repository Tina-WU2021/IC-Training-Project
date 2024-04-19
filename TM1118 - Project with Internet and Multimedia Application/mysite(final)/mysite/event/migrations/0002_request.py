# Generated by Django 3.2.6 on 2022-07-12 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(choices=[('W311-H1', 'W311-H1'), ('W311-H2', 'W311-H2'), ('W311-H3', 'W311-H3'), ('W311a', 'W311a'), ('W311b', 'W311b'), ('W311d-Z1', 'W311d-Z1'), ('W311d-Z2', 'W311d-Z2')], max_length=10)),
                ('start', models.DateField(verbose_name='From:')),
                ('end', models.DateField(verbose_name='To:')),
            ],
        ),
    ]