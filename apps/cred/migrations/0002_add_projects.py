import apps.cred.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('cred', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128, verbose_name='Title')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('icon', apps.cred.fields.SizedImageFileField(blank=True, null=True, upload_to='icons/project', verbose_name='Icon')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='cred',
            name='project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cred.Project', verbose_name='Project'),
        ),
    ]
