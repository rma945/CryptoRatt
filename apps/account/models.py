import uuid
import hmac

from django.db import models
from django import forms
from django.forms import ModelForm, SelectMultiple, Select, CheckboxInput
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.utils import timezone

from django_otp import user_has_device

from tastypie.compat import AUTH_USER_MODEL
from datetime import timedelta

from apps.cred.models import Tag

from hashlib import sha1


def is_2fa_enabled(self):
    '''Returns user 2fa active status'''
    return user_has_device(self)

class LDAPPassChangeForm(SetPasswordForm):
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)

    def clean_old_password(self):
        from django_auth_ldap.backend import LDAPBackend

        old_password = self.cleaned_data["old_password"]
        u = LDAPBackend().authenticate(self.user.username, old_password)
        if u is None:
            raise forms.ValidationError(_("Incorrect password"))
        return old_password

    def save(self):
        old_password = self.cleaned_data["old_password"]
        new_password = self.cleaned_data["new_password1"]

        conn = self.user.ldap_user._get_connection()
        conn.simple_bind_s(self.user.ldap_user.dn, old_password.encode('utf-8'))
        conn.passwd_s(self.user.ldap_user.dn, old_password.encode('utf-8'), new_password.encode('utf-8'))

        return self.user

LDAPPassChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    items_per_page = models.IntegerField(verbose_name=_('Items at page'), default=25)
    favourite_tags = models.ManyToManyField(Tag, verbose_name=_('Favourite tags'), blank=True)
    # favourite_credentials = models.ManyToManyField(Cred, verbose_name=_('Favourite tags'), blank=True)
    # favourite_projects = models.ManyToManyField(Cred, verbose_name=_('Favourite tags'), blank=True)
    password_changed = models.DateTimeField(default=now)
    avatar = models.BinaryField(null=True, default=None)
    favourite_menu = models.BooleanField(default=False, verbose_name=_('Enable favorites menu'))
    theme = models.CharField(max_length=128, default='bootstrap.default.min.css', verbose_name=_('Theme'))

    def __str__(self):
        return self.user.username

# TODO: move to form.py
class UserProfileForm(ModelForm):
    class Meta:
        custom_themes = [
            ('bootstrap.default.min.css', 'Default'),
            ('bootstrap.cosmo.min.css', 'Cosmo'),
            ('bootstrap.cerulean.min.css', 'Cerulean'),
            ('bootstrap.darkly.min.css', 'Darkly'),
            ('bootstrap.flatly.min.css', 'Flatly'),
            ('bootstrap.litera.min.css', 'Litera'),
            ('bootstrap.pulse.min.css', 'Pulse'),
            ('bootstrap.lux.min.css', 'Lux'),
            ('bootstrap.lumen.min.css', 'Lumen'),
            ('bootstrap.litera.min.css', 'Litera'),
            ('bootstrap.slate.min.css', 'Slate'),
            ('bootstrap.spacelab.min.css', 'Spacelab'),
        ]

        model = UserProfile
        exclude = ('user', 'password_changed',)
        widgets = {
            'favourite_menu': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'favourite_tags': SelectMultiple(attrs={'class': 'single-select'}),
            'theme': Select(
                choices=custom_themes,
                attrs={'class': 'form-control single-select'}),
            'items_per_page': Select(
                choices=[('10', 10), ('20', 20), ('30', 30), ('40', 40), ('50', 50)],
                attrs={'class': 'form-control single-select'}),
        }


# Attach the UserProfile object to the User
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


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
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='rattic_api_key', on_delete=models.DO_NOTHING)
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


class ApiKeyForm(ModelForm):
    class Meta:
        model = ApiKey
        exclude = ('user', 'key', 'active', 'created', 'expires')

    def save(self):
        if self.instance.expires < self.instance.created + timedelta(minutes=1):
            self.instance.expires = self.instance.created
        return super(ApiKeyForm, self).save()


admin.site.register(UserProfile)
