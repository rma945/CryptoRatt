import apps.cred.fields
from django.conf import settings
from django.db import migrations, models, connection
from base64 import b64decode
import django.db.models.deletion

def migrate_attachments(apps, schema_editor):
    '''
    convert legacy attachment \ ssh_keys to a new attachment model
    legacy attachments was stored as base64 encoded string
    new attachments stores as default BinaryField
    '''

    Credentials = apps.get_model('cred', 'Cred')
    sql_cursor = connection.cursor()

    for c in Credentials.objects.raw('SELECT * FROM cred_cred'):
        if c.attachment:
            a_id = c.attachment.split(".")[0]
            sql_cursor.execute('''SELECT content FROM database_files_file where id={0};'''.format(a_id))
            sql_raw_content = sql_cursor.fetchone()[0]
            if sql_raw_content:
                attachment = apps.get_model('cred', 'Attachment')
                attachment(credential=c, filename=c.attachment_name, content=b64decode(sql_raw_content)).save()

        if c.ssh_key:
            a_id = c.ssh_key.split(".")[0]
            sql_cursor.execute('''SELECT content FROM database_files_file where id={0};'''.format(a_id))
            sql_raw_content = sql_cursor.fetchone()[0]
            if sql_raw_content:
                attachment = apps.get_model('cred', 'Attachment')
                attachment(credential=c, filename=c.ssh_key_name, content=b64decode(sql_raw_content)).save()

class Migration(migrations.Migration):

    dependencies = [
        ('cred', '0001_initial'),
        ('cred', '0002_add_projects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=256, verbose_name='Filename')),
                ('mime', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Mime')),
                ('content', models.BinaryField(default=None, null=True)),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cred.Cred')),
            ],
        ),
        migrations.AlterField(
            model_name='Cred',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group', verbose_name='Group'),
        ),       
        migrations.AlterField(
            model_name='Cred',
            name='latest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='cred.Cred'),
        ),       
        migrations.AlterField(
            model_name='CredChangeQ',
            name='cred',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cred.Cred'),
        ),       
        migrations.AlterField(
            model_name='CredAudit',
            name='cred',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='cred.Cred'),
        ),       
        migrations.AlterField(
            model_name='CredAudit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credlogs', to=settings.AUTH_USER_MODEL),
        ),       
        migrations.AlterField(
            model_name='credaudit',
            name='audittype',
            field=models.CharField(choices=[('A', 'Added'), ('C', 'Changed'), ('M', 'Only Metadata Changed'), ('V', 'Only Details Viewed'), ('X', 'Exported'), ('D', 'Deleted'), ('S', 'Scheduled For Change'), ('P', 'Password Viewed'), ('AD', 'Attachment Added'), ('AV', 'Attachment Viewed'), ('AD', 'Attachment Deleted')], max_length=5),
        ),
        migrations.RunPython(migrate_attachments),
    ]
