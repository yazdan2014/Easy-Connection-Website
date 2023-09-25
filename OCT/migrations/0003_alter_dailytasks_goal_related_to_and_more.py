# Generated by Django 4.2.5 on 2023-09-23 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OCT', '0002_rename_tasks_dailytasks_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytasks',
            name='goal_related_to',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='goal_related_to', to='OCT.monthlytasks'),
        ),
        migrations.AlterField(
            model_name='oct',
            name='daily_tasks',
            field=models.ManyToManyField(blank=True, to='OCT.dailytasks'),
        ),
        migrations.AlterField(
            model_name='oct',
            name='monthly_tasks',
            field=models.ManyToManyField(blank=True, to='OCT.monthlytasks'),
        ),
    ]
