# Generated by Django 2.2 on 2019-05-20 16:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cred', '0005_project_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
