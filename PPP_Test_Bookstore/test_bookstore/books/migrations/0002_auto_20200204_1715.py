# Generated by Django 3.0.2 on 2020-02-04 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_format',
        ),
        migrations.AddField(
            model_name='book',
            name='book_formats',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
    ]