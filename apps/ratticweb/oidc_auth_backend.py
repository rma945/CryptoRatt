from django.conf import settings
from django.contrib.auth import get_backends
from django.contrib.auth.models import Group

from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.utils.module_loading import import_string

from requests.exceptions import HTTPError

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from mozilla_django_oidc.utils import (
    import_from_settings,
    parse_www_authenticate_header,
)

def SyncUserGroups(user, claims):
    """
    Sync local user groups with groups from OIDC claims
    Create new groups if they not exists
    Add user to staff group, if staff group exists in claims
    """

    for g in claims.get('groups', []):
        group, is_created = Group.objects.get_or_create(name=g)
        
        if is_created:
            user.groups.add(group)
        else:
            if not user.groups.filter(name=g).exists():
                user.groups.add(group)

    # remove user from old groups
    for g in user.groups.all():
        if g.name not in claims.get('groups', []):
            g.user_set.remove(user)
    
    return user


class OIDCAuthBackend(OIDCAuthenticationBackend):
    """
    Custom OIDC based authentification backend
    """

    

    # custom user creation function, with updating all default user fields
    def create_user(self, claims):
        user = super(OIDCAuthBackend, self).create_user(claims)
        user.username = claims.get("preferred_username", "")
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.is_staff = settings.OIDC_ADMIN_GROUP in claims.get('groups', [])
        user = SyncUserGroups(user, claims)
        user.save()

        return user

    # custom user update function, with updating all default user fields
    def update_user(self, user, claims):
        user.username = claims.get("preferred_username", "")
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.is_staff = settings.OIDC_ADMIN_GROUP in claims.get('groups', [])
        user = SyncUserGroups(user, claims)
        user.save()

        return user
