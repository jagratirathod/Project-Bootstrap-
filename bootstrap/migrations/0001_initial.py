# Generated by Django 3.1.6 on 2021-09-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('regid', models.AutoField(primary_key=True, serialize=False)),
                ('firstnm', models.CharField(max_length=100)),
                ('lastnm', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=10)),
                ('mobile', models.CharField(max_length=12)),
                ('info', models.CharField(max_length=100)),
                ('status', models.IntegerField()),
                ('role', models.CharField(max_length=10)),
            ],
        ),
    ]
