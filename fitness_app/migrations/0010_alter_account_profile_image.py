# Generated by Django 5.0.7 on 2024-08-13 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0009_rename_review_reviewontrainers_reviewonwebsite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.FileField(upload_to='fitness_app_image'),
        ),
    ]
