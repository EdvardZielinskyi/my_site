# Generated by Django 4.1.2 on 2022-11-14 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(max_length=200),
        ),
    ]
