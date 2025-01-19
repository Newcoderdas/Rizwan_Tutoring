# Generated by Django 5.1 on 2024-09-13 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_exercise_correct_solution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='correct_solution',
            field=models.TextField(default='Default solution'),
        ),
        migrations.AddField(
            model_name='submission',
            name='answer_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='main.exercise'),
        ),
    ]
