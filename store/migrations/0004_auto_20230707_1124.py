# Generated by Django 3.2.11 on 2023-07-07 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20230707_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cores',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='graphics',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='memory',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
