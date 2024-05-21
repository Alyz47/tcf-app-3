# Generated by Django 5.0.4 on 2024-05-20 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0014_alter_subcategory_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='gender',
            field=models.CharField(blank=True, choices=[('men', 'Men'), ('women', 'Women'), ('others', 'Others')], max_length=25, null=True),
        ),
    ]
