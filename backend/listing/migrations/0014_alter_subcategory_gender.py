# Generated by Django 5.0.4 on 2024-05-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0013_listing_gender_alter_subcategory_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='gender',
            field=models.CharField(blank=True, choices=[('men', 'Men'), ('women', 'Women')], default='Undefined', max_length=25, null=True),
        ),
    ]
