# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-03-18 11:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challengeTitle', models.TextField()),
                ('challengeDescription', models.TextField()),
                ('challengeCreatedAt', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('challengeDeadline', models.DateField()),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileCaption', models.TextField()),
                ('uploadedAt', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('filePath', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predicateapp.Challenge')),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submittedAt', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('predictionDescription', models.TextField()),
                ('score', models.TextField(null=True)),
                ('scoreUpdatedAt', models.TextField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predicateapp.Challenge')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.TextField()),
                ('lastName', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('userType', models.TextField(default='General')),
                ('username', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('score', models.TextField(default='0')),
                ('verificationCode', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='prediction',
            name='submittedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predicateapp.User'),
        ),
    ]
