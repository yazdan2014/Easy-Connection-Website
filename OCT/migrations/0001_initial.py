# Generated by Django 4.2.5 on 2023-09-23 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=150)),
                ('tasks', models.TextField()),
                ('estimated_time', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(max_length=150)),
                ('progress_percentage', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='OCT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_tasks', models.ManyToManyField(to='OCT.dailytasks')),
                ('monthly_tasks', models.ManyToManyField(to='OCT.monthlytasks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='octuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dailytasks',
            name='goal_related_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal_related_to', to='OCT.monthlytasks'),
        ),
    ]
