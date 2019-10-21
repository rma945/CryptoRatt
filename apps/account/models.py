import uuid
import hmac

from django.db import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.utils import timezone
from django.contrib.sessions.base_session import AbstractBaseSession

from django_otp import user_has_device

from tastypie.compat import AUTH_USER_MODEL
from datetime import timedelta

from apps.cred.models import Tag, Project, Cred

from hashlib import sha1


def is_2fa_enabled(self):
    '''Returns user 2fa active status'''
    return user_has_device(self)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items_per_page = models.IntegerField(verbose_name=_('Items at page'), default=25)
    favourite_tags = models.ManyToManyField(Tag, verbose_name=_('Favourite tags'), blank=True)
    favourite_credentials = models.ManyToManyField(Cred, verbose_name=_('Favourite credentials'), blank=True)
    favourite_projects = models.ManyToManyField(Project, verbose_name=_('Favourite projects'), blank=True)
    password_changed = models.DateTimeField(default=now)
    avatar = models.BinaryField(null=True, default=None, verbose_name=_('Profile avatar'))
    theme = models.CharField(max_length=128, default='bootstrap.default.min.css', verbose_name=_('Theme'))

    def __str__(self):
        return self.user.username

### TODO: REPLACE THIS
User.profile = property(lambda u: UserProfile.objects.get(user=u))

@receiver(pre_save, sender=User)
def user_save_handler(sender, instance, **kwargs):
    try:
        olduser = User.objects.get(id=instance.id)
    except User.DoesNotExist:
        return
    if olduser.password != instance.password:
        p = instance.profile
        p.password_changed = now()
        p.save()

class ApiKey(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='rattic_api_key', null=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=128, blank=True, default='', db_index=True)
    name = models.CharField(max_length=128, blank=True, default='unknown')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now)
    expires = models.DateTimeField(default=now)

    @classmethod
    def expired(kls, user):
        return ApiKey.objects.filter(user=user, expires__gt=F("created")).filter(expires__lt=timezone.now())

    @classmethod
    def delete_expired(kls, user):
        for gone in kls.expired(user):
            gone.delete()

    def __str__(self):
        return u"%s for %s" % (self.key, self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        # Get a random UUID.
        new_uuid = uuid.uuid4()
        # Hmac that beast.
        return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()

    @property
    def has_expiry(self):
        return self.expires > self.created

class UserSession(AbstractBaseSession):
    """Custom user session model with account_id as session key"""
    user_id = models.IntegerField(null=True, db_index=True)
    created = models.DateTimeField(auto_now=True)
    user_agent = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=128, blank=True, null=True)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

admin.site.register(UserProfile)