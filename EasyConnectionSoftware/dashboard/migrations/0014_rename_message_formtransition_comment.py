# Generated by Django 4.2.5 on 2023-11-04 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_formtransition_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formtransition',
            old_name='message',
            new_name='comment',
        ),
    ]
