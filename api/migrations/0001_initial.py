# Generated by Django 5.1.4 on 2025-01-13 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('url_avatar', models.CharField(max_length=100)),
                ('win', models.IntegerField()),
                ('lose', models.IntegerField()),
            ],
        ),
    ]
