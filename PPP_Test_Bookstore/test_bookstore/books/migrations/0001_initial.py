# Generated by Django 3.0.2 on 2020-02-02 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('authors', models.CharField(max_length=200)),
                ('isbn_13', models.CharField(max_length=13)),
                ('subtitle', models.CharField(blank=True, default='', max_length=200)),
                ('series', models.CharField(blank=True, default='', max_length=200)),
                ('volume', models.CharField(blank=True, default='', max_length=3)),
                ('desc', models.TextField()),
                ('book_format', models.CharField(choices=[('H', 'Hardcover'), ('P', 'Paperback'), ('E', 'Ebook'), ('A', 'Audio')], max_length=1)),
                ('sale_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
