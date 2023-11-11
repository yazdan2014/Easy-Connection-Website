# Generated by Django 4.2.5 on 2023-11-08 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_alter_userform_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formtransition',
            name='status',
            field=models.CharField(choices=[('edit', 'Must Be Edited'), ('sb', 'Sent Back'), ('ac', 'Accepted'), ('dc', 'Declined')], default='og', max_length=150, null=True),
        ),
    ]
