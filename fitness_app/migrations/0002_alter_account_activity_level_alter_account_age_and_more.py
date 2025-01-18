# Generated by Django 5.0.6 on 2024-07-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='activity_level',
            field=models.CharField(blank=True, choices=[('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'), ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Super Active', 'Super Active')], default='Moderately Active', max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='experience_level',
            field=models.CharField(blank=True, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='fitness_goal',
            field=models.CharField(blank=True, choices=[('Lose Weight', 'Lose Weight'), ('Gain Muscle', 'Gain Muscle'), ('Maintain Fitness', 'Maintain Fitness')], default='Gain Muscle', max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='height',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='weight',
            field=models.FloatField(blank=True),
        ),
    ]
