# Generated by Django 4.2.11 on 2024-08-04 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="theme_preference",
            field=models.CharField(
                choices=[("light", "Light"), ("dark", "Dark"), ("system", "System")],
                default="system",
                max_length=10,
            ),
        ),
    ]