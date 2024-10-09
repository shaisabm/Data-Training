# Generated by Django 4.2.16 on 2024-10-08 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=100, null=True)),
                ('zoom_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('registration_time', models.DateTimeField()),
                ('approved', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=100)),
                ('participated', models.BooleanField(blank=True, default=False, null=True)),
                ('event_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to='dashboard.event')),
                ('zoom_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zoom_registrations', to='dashboard.event')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('joined_time', models.DateTimeField()),
                ('leave_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('guest', models.BooleanField(default=False)),
                ('in_waiting_room', models.BooleanField(default=False)),
                ('event_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_participants', to='dashboard.event')),
                ('zoom_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zoom_participants', to='dashboard.event')),
            ],
        ),
    ]