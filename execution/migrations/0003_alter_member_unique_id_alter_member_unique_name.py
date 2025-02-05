# Generated by Django 5.0.4 on 2025-02-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0002_member_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='unique_id',
            field=models.CharField(default='generateID', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='unique_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
