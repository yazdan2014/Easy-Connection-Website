# Generated by Django 4.2.5 on 2023-09-23 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OCT', '0003_alter_dailytasks_goal_related_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytasks',
            name='goal_related_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goal_related_to', to='OCT.monthlytasks'),
        ),
    ]
