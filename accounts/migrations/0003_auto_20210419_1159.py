# Generated by Django 3.2 on 2021-04-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210413_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='phone_no',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_no',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
