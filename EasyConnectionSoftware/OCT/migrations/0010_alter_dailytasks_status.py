# Generated by Django 4.2.5 on 2023-10-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCT', '0009_monthlytasks_status_alter_dailytasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytasks',
            name='status',
            field=models.CharField(choices=[('jc', 'Just Created'), ('og', 'On Going'), ('cba', 'Checked By Admin'), ('edt', 'Edited'), ('done', 'Done'), ('nd', 'Not Done')], default='jc', max_length=150),
        ),
    ]