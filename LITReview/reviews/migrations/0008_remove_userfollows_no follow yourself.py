# Generated by Django 4.0 on 2022-01-14 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_userfollows_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollows',
            name='no follow yourself',
        ),
    ]
