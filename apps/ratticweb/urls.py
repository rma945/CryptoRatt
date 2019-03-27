import django_saml2_auth.views
import django_saml2_auth.urls
from two_factor.urls import urlpatterns as django_twofactor_urls
import django.contrib.admindocs.urls
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from apps.cred.api import CredResource, TagResource
from apps.staff.api import GroupResource
from django.conf import settings

import apps.ratticweb.views
import apps.account.urls
import apps.cred.urls
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

base_urlpatterns = []

# SAML
if settings.SAML_ENABLED:
    base_urlpatterns += [
        path('saml2_auth/', include(django_saml2_auth.urls)),
        path('accounts/login/', django_saml2_auth.views.signin),
    ]

# Setup the base paths for applications, and the API
base_urlpatterns += [
    # Apps:
    path('', apps.ratticweb.views.home, name='home'),
    path('account/', include(apps.account.urls), name='account'),
    path('cred/', include(apps.cred.urls), name='cred'),
    path('staff/', include(apps.staff.urls), name='staff'),
    path('help/', include(apps.help.urls), name='help'),

    # API
    path('api/', include(v1_api.urls)),

    # Language
    # (r'^i18n/', i18n),

    # two Factor
    path('', include(django_twofactor_urls)),
]

# If debug mode - enable the Django admin interface
if settings.DEBUG:
    from django.contrib import admin
    admin.autodiscover()
    base_urlpatterns += [
        path('admin/', admin.site.urls)
    ]

    if settings.SAML_ENABLED:
        base_urlpatterns += [
            path('admin/login/', django_saml2_auth.views.signin),
        ]
        

# Strip any leading slash from the RATTIC_ROOT_URL
if settings.RATTIC_ROOT_URL[0] == '/':
    root = settings.RATTIC_ROOT_URL[1:]
else:
    root = settings.RATTIC_ROOT_URL

# Serve RatticDB from an alternate root if requested
urlpatterns = [
    path('' + root, include(base_urlpatterns)),
]

# Serve the static files from the right location in dev mode
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        path('media/<slug:path>', django.views.static.serve, {'document_root': settings.MEDIA_ROOT})
    ]