# Generated by Django 4.2 on 2023-05-08 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ref_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
