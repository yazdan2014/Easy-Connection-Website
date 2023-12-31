# Generated by Django 4.2.5 on 2023-11-04 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_rename_message_formtransition_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='formtransition',
            name='prev_transition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev', to='dashboard.formtransition'),
        ),
        migrations.AlterField(
            model_name='formtransition',
            name='next_transition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='dashboard.formtransition'),
        ),
    ]
