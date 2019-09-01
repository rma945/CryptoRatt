from two_factor.urls import urlpatterns as django_twofactor_urls
import django.contrib.admindocs.urls
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from apps.cred.api import CredResource, TagResource
from apps.staff.api import GroupResource
from django.conf import settings

import apps.ratticweb.views
import apps.account.urls
import apps.cred.urls, apps.cred.views
import apps.staff.urls
import apps.help.urls

app_name = "ratticweb"

# Configure the error handlers
handler500 = 'apps.ratticweb.views.handle500'
handler404 = 'apps.ratticweb.views.handle404'

# Setup the API
v1_api = Api(api_name='v1')
v1_api.register(CredResource())
v1_api.register(TagResource())
v1_api.register(GroupResource())

urlpatterns = []

# If debug mode - enable the Django admin interface for password reset
if not settings.LDAP_ENABLED and not settings.SSO_ENABLED or settings.DEBUG:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls)
    ]

# Enable SSO
if settings.SSO_ENABLED:
    urlpatterns += [
        re_path(r'^oidc/', include('mozilla_django_oidc.urls')),
    ]

# Setup the base paths for applications, and the API
urlpatterns += [
    # Apps:
    path('', apps.ratticweb.views.home, name='home'),
    path('account/', include(apps.account.urls), name='account'),
    path('cred/', include(apps.cred.urls), name='cred'),
    path('staff/', include(apps.staff.urls), name='staff'),
    path('help/', include(apps.help.urls), name='help'),
 
    # API
    path('api/', include(v1_api.urls)),

    # render base64 encoded icons as static TODO: move to api
    path('api/static/rattic/img/icons/<int:cred_id>.png', apps.cred.views.get_icon, name='render_credential_icon' ),

    # Language
    # (r'^i18n/', i18n),

    # two Factor
    path('', include(django_twofactor_urls)),
]


# Serve the static files from the right location in dev mode
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        path('media/<slug:path>', django.views.static.serve, {'document_root': settings.MEDIA_ROOT})
    ]