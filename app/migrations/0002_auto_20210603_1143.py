# Generated by Django 3.2.4 on 2021-06-03 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discription',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='discounted_prince',
            new_name='discounted_price',
        ),
    ]
