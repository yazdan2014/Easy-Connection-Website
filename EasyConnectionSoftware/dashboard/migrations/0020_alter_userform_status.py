# Generated by Django 4.2.5 on 2023-11-08 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_alter_userform_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userform',
            name='status',
            field=models.CharField(choices=[('og', 'On Going'), ('sm', 'Submitted'), ('dc', 'Declined')], default='og', max_length=50),
        ),
    ]
