# Generated by Django 4.2.11 on 2024-08-02 17:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ("users", "0001_initial"),
=======
        ('users', '0001_initial'),
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    ]

    operations = [
        migrations.AddField(
<<<<<<< HEAD
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                related_name="following", to=settings.AUTH_USER_MODEL
            ),
=======
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following', to=settings.AUTH_USER_MODEL),
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
        ),
    ]
