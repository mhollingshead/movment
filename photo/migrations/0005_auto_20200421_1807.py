# Generated by Django 3.0.5 on 2020-04-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0004_commentpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentpost',
            name='video',
        ),
        migrations.AddField(
            model_name='commentpost',
            name='video_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
