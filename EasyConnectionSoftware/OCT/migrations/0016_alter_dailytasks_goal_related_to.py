# Generated by Django 4.2.5 on 2023-10-21 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OCT', '0015_alter_dailytasks_checked_by_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytasks',
            name='goal_related_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goal_related_to', to='OCT.monthlytasks'),
        ),
    ]
