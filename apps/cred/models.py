from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
from django.utils.timezone import now
from django.conf import settings
from django.templatetags.static import static

from apps.ratticweb.util import DictDiffer, field_file_compare
from apps.cred.fields import SizedImageFileField

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    
    def credentials_count(self):
        return Cred.objects.filter(tags=self).count()

    def visible_count(self, user):
        return Cred.cred.objects.visible(user).filter(tags=self).count()

class CredIconAdmin(admin.ModelAdmin):
    list_display = ('name', 'filename')


class SearchManager(models.Manager):
    def visible(self, user, historical=False, deleted=False):
        usergroups = user.groups.all()
        qs = super(SearchManager, self).get_queryset()

        if not user.is_staff or not deleted:
            qs = qs.exclude(is_deleted=True, latest=None)

        if not historical:
            qs = qs.filter(latest=None)

        # return all secrets if user in a staff group
        if user.is_staff:
            return qs
        else:
            qs = qs.filter(Q(group__in=usergroups)
                        | Q(latest__group__in=usergroups)
                        | Q(groups__in=usergroups)
                        | Q(users__in=[user.id])
                        | Q(latest__groups__in=usergroups)).distinct()

        return qs

    def change_advice(self, user, grouplist=[]):
        logs = CredAudit.objects.filter(
            # Get a list of changes done
            Q(cred__group__in=grouplist, audittype=CredAudit.CREDCHANGE) |
            # Combined with a list of views from this user
            Q(cred__group__in=grouplist, audittype__in=[CredAudit.CREDVIEW, CredAudit.CREDPASSVIEW, CredAudit.CREDADD, CredAudit.CREDEXPORT], user=user)
        ).order_by('time', 'id')

        # Go through each entry in time order
        tochange = []
        for l in logs:
            # If this user viewed the password then change it
            if l.audittype in (CredAudit.CREDVIEW, CredAudit.CREDPASSVIEW, CredAudit.CREDADD, CredAudit.CREDEXPORT):
                tochange.append(l.cred.id)
            # If there was a change done not by this user, dont change it
            if l.audittype == CredAudit.CREDCHANGE and l.user != user:
                if l.cred.id in tochange:
                    tochange.remove(l.cred.id)

        # Fetch the list of credentials to change from the DB for the view
        return Cred.objects.filter(id__in=tochange)

class Project(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128, db_index=True)
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True)
    icon = models.BinaryField(null=True, default=None)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    def getAllCreds(self):
        return self.cred_set.filter(latest=None)

    def delete(self):
        self.cred_set.update(project=None, is_expired=True)
        super(Project, self).delete()

    def __str__(self):
        return self.title

class Cred(models.Model):
    METADATA = ('project', 'description', 'descriptionmarkdown', 'group', 'groups', 'tags', 'iconname', 'latest', 'id', 'modified')
    SORTABLES = ('title', 'username', 'group', 'id', 'modified')
    APP_SET = ('is_deleted', 'latest', 'modified', 'attachments')
    objects = SearchManager()

    # User changable fields
    project = models.ForeignKey(Project, verbose_name=_('Project'), blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)
    title = models.CharField(verbose_name=_('Title'), max_length=64, db_index=True)
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True, db_index=True)
    username = models.CharField(verbose_name=_('Username'), max_length=250, blank=True, null=True, db_index=True)
    password = models.CharField(verbose_name=_('Password'), max_length=250, blank=True, null=True)
    descriptionmarkdown = models.BooleanField(verbose_name=_('Markdown Description'), default=True, )
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name=_('Group'), blank=True, null=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(Group, verbose_name=_('Groups'), related_name="child_creds", blank=True, default=None)
    users = models.ManyToManyField(User, verbose_name=_('Users'), related_name="child_creds", blank=True, default=None)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'), related_name='child_creds', blank=True, default=None)
    iconname = models.CharField(verbose_name=_('Icon'), default='Key.png', max_length=64)

    # Application controlled fields
    is_deleted = models.BooleanField(default=False, db_index=True)
    is_expired = models.BooleanField(default=False, db_index=True)
    latest = models.ForeignKey('Cred', related_name='history', blank=True, null=True, db_index=True, on_delete=models.SET_NULL)
    modified = models.DateTimeField(db_index=True, auto_now_add=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            # Get a copy of the old object from the db
            old = Cred.objects.get(id=self.id)

            # Reset the primary key so Django thinks its a new object
            old.id = None

            # Set the latest on the old copy to the new copy
            old.latest = self

            # Create it in the DB
            old.save()

            # Add the tags to the old copy now that it exists
            for t in self.tags.all():
                old.tags.add(t)

            # Add the groups
            for g in self.groups.all():
                old.groups.add(g)

            # Lets see what was changed
            oldcred = model_to_dict(old)
            newcred = model_to_dict(self)
            diff = DictDiffer(newcred, oldcred).changed()

            # Check if some non-metadata was changed
            chg = diff - set(Cred.METADATA)
            cred_changed = len(chg) > 0

            # If the creds were changed update the modify date
            if cred_changed:
                self.modified = now()
        except Cred.DoesNotExist:
            # This just means its new cred, set the initial modified time
            self.modified = now()

        super(Cred, self).save(*args, **kwargs)

    def delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()
        else:
            super(Cred, self).delete()

    def on_changeq(self):
        return CredChangeQ.objects.filter(cred=self).exists()

    def is_latest(self):
        return self.latest is None

    def is_owned_by(self, user):
        # Staff can do anything
        if user.is_staff:
            return True

        # If its the latest and in your group you can see it
        if not self.is_deleted and self.latest is None and self.group in user.groups.all():
            return True

        # If the latest is in your group you can see it
        if not self.is_deleted and self.latest is not None and self.latest.group in user.groups.all():
            return True

        return False

    def is_visible_by(self, user):
        # Staff can see anything
        if user.is_staff:
            return True

        # If its not deleted
        if not self.is_deleted:

            # get latest version of credentials object
            if self.latest is None:
                cred_latest = self
            else:
                cred_latest = self.latest

            # if it have a personal share
            if user in cred_latest.users.all():
                return True

            # if it in your group or it belongs to a viewer group you can see it
            if cred_latest.group in user.groups.all() or any([g in user.groups.all() for g in cred_latest.groups.all()]):
                return True

        return False

    def __str__(self):
        return self.title

class Attachment(models.Model):
    credential = models.ForeignKey(Cred, on_delete=models.CASCADE)
    filename = models.CharField(verbose_name=_('Filename'), max_length=256)
    created = models.DateTimeField(auto_now_add=True, null=True)
    mime = models.CharField(verbose_name=_('Mime'), max_length=64, blank=True, null=True, default=None)
    content = models.BinaryField(null=True, default=None)

    def __str__(self):
        return self.filename

    # TODO: get_icon - rewrite this function
    def get_icon(self): 
        icon = static("rattic/img/attachment-default.png")

        if self.mime:
            if self.mime in ('application/x-x509-ca-cert', 'application/x-x509-user-cert'):
                icon = static("rattic/img/attachment-sshkey.png")
            elif self.mime in ('application/pkix-crl','application/x-pkcs12', 'application/x-iwork-keynote-sffkey', 'application/pkix-cert', 'application/pkcs10'):
                icon = static("rattic/img/attachment-certificate.png")
            elif self.mime in ('image/png', 'image/jpeg', 'image/gif'):
                icon = static("rattic/img/attachment-image.png")
            elif self.mime in ('application/zip', 'application/x-bzip', 'application/x-tar'):
                icon = static("rattic/img/attachment-archive.png")

        return icon


class CredAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'group')


class CredAudit(models.Model):
    CREDADD = 'A'
    CREDCHANGE = 'C'
    CREDMETACHANGE = 'M'
    CREDVIEW = 'V'
    CREDEXPORT = 'X'
    CREDPASSVIEW = 'P'
    CREDDELETE = 'D'
    CREDUNDELETE = 'R'
    CREDSCHEDCHANGE = 'S'
    CREDATTACHADDED = 'AD'
    CREDATTACHVIEW = 'AV'
    CREDATTACHDELETED = 'AD'

    CREDAUDITCHOICES = (
        (CREDADD, _('Added')),
        (CREDCHANGE, _('Changed')),
        (CREDMETACHANGE, _('Only Metadata Changed')),
        (CREDVIEW, _('Only Details Viewed')),
        (CREDEXPORT, _('Exported')),
        (CREDDELETE, _('Deleted')),
        (CREDUNDELETE, _('Restored')),
        (CREDSCHEDCHANGE, _('Scheduled For Change')),
        (CREDPASSVIEW, _('Password Viewed')),
        (CREDATTACHADDED, _('Attachment Added')),
        (CREDATTACHVIEW, _('Attachment Viewed')),
        (CREDATTACHDELETED, _('Attachment Deleted')),
    )

    audittype = models.CharField(max_length=5, choices=CREDAUDITCHOICES)
    cred = models.ForeignKey(Cred, related_name='logs', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='credlogs', null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        get_latest_by = 'time'
        ordering = ('-time',)


class CredAuditAdmin(admin.ModelAdmin):
    list_display = ('audittype', 'user', 'cred', 'time')


class CredChangeQManager(models.Manager):
    def add_to_changeq(self, cred):
        return self.get_or_create(cred=cred)

    def for_user(self, user):
        return self.filter(cred__in=Cred.objects.visible(user))


class CredChangeQ(models.Model):
    objects = CredChangeQManager()
    cred = models.ForeignKey(Cred, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)


class CredChangeQAdmin(admin.ModelAdmin):
    list_display = ('cred', 'time')


admin.site.register(CredAudit, CredAuditAdmin)
admin.site.register(Cred, CredAdmin)
admin.site.register(Tag)
admin.site.register(CredChangeQ, CredChangeQAdmin)
