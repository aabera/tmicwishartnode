# Generated by Django 4.2 on 2023-05-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='analysis_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='category',
            field=models.CharField(default='cat', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sample_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
