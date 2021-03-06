# Generated by Django 3.2.7 on 2021-09-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('item_name', models.CharField(blank=True, max_length=255, null=True)),
                ('item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('item_class', models.CharField(blank=True, max_length=255, null=True)),
                ('item_score', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'item',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('item_name', models.CharField(blank=True, max_length=255, null=True)),
                ('item_score', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'recommend',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('item_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('item_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('item_score', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_passward', models.CharField(blank=True, max_length=255, null=True)),
                ('user_email', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
