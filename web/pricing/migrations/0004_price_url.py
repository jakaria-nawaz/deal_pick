# Generated by Django 2.2.1 on 2019-05-23 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0003_auto_20190522_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='url',
            field=models.URLField(null=True),
        ),
    ]