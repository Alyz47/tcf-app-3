# Generated by Django 5.0.4 on 2024-05-17 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_has_preference_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='has_card',
            field=models.BooleanField(default=False),
        ),
    ]