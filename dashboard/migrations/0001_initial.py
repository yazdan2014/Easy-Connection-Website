# Generated by Django 4.2.5 on 2023-09-20 12:13

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.CharField(max_length=80, unique=True)),
                ('username', models.CharField(max_length=45, unique=True)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('role', models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Physician', 'Physician')], max_length=45)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FormSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('descrition', models.TextField()),
                ('fields', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserForm',
            fields=[
                ('descrition', models.TextField()),
                ('form_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('fields', models.JSONField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('current_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_receiver', to=settings.AUTH_USER_MODEL)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sample', to='dashboard.formsample')),
            ],
        ),
        migrations.CreateModel(
            name='FormTransition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('message', models.TextField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.userform')),
                ('receiver_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]