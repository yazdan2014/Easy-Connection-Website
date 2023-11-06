# Generated by Django 4.2.5 on 2023-10-30 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_formtransition_receiver_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formtransition',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.userform'),
        ),
        migrations.AddField(
            model_name='formtransition',
            name='receiver_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formtransition',
            name='sender_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userform',
            name='transitions',
            field=models.ManyToManyField(to='dashboard.formtransition'),
        ),
    ]