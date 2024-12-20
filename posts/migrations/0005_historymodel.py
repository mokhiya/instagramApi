# Generated by Django 5.1.3 on 2024-11-16 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_commentmodel_parent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField()),
                ('visibility', models.CharField(choices=[('followers', 'Followers'), ('public', 'Public'), ('private', 'Private')], default='followers', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'Histories',
                'ordering': ['timestamp'],
            },
        ),
    ]
