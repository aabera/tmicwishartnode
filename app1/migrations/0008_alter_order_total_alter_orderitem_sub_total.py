# Generated by Django 4.2 on 2023-05-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_orderitem_sub_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sub_total',
            field=models.FloatField(),
        ),
    ]