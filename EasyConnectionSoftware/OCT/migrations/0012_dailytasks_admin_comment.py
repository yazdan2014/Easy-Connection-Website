# Generated by Django 4.2.5 on 2023-10-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCT', '0011_monthlytasks_admin_comment_alter_monthlytasks_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailytasks',
            name='admin_comment',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]