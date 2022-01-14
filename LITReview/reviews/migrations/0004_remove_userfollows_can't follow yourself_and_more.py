# Generated by Django 4.0 on 2022-01-14 11:59

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', "0003_userfollows_can't follow yourself"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollows',
            name="can't follow yourself",
        ),
        migrations.AddConstraint(
            model_name='userfollows',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('followed_user')), _negated=True), name="can't follow yourself"),
        ),
    ]
