# Generated by Django 3.1 on 2021-06-28 21:25

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(null=True, upload_to=post.models.user_directory_path, verbose_name='Picture'),
        ),
    ]
