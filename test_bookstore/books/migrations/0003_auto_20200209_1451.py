# Generated by Django 3.0.2 on 2020-02-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20200204_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_formats',
            field=models.CharField(max_length=60),
        ),
    ]