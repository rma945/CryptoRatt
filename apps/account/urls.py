from two_factor.views import QRGeneratorView
from django.urls import include, path, re_path
from django.conf import settings
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordChangeDoneView,
    PasswordResetConfirmView
)

from apps.account.views import (
    profile, newapikey, deleteapikey, RatticSessionDeleteView,
    RatticTFADisableView, RatticTFABackupTokensView,
    RatticTFASetupView, RatticTFALoginView, RatticTFAGenerateApiKey,
    rattic_change_password,ldap_password_change,
)

app_name = "account"

urlpatterns = [
    path('', profile, {}, name='profile'),
    path('newapikey/', newapikey, {}, name="new_api_key"),
    path('deleteapikey/<int:key_id>/', deleteapikey, {}, name="delete_api_key"),

    path('login/', RatticTFALoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.RATTIC_ROOT_URL}, name="logout"),

    path('killsession/<slug:pk>/', RatticSessionDeleteView.as_view(), {'next_page': settings.RATTIC_ROOT_URL}, name='kill_session'),

    path('generate_api_key', RatticTFAGenerateApiKey.as_view(), name="generate_api_key"),
    path('two_factor/disable/', RatticTFADisableView.as_view(), name='tfa_disable'),
    path('two_factor/backup/', RatticTFABackupTokensView.as_view(), name='tfa_backup'),
    path('two_factor/setup/', RatticTFASetupView.as_view(), name='tfa_setup'),
    path('two_factor/qr/', QRGeneratorView.as_view(), name='tfa_qr'),
]

# URLs we don't want enabled with LDAP
if not settings.LDAP_ENABLED and not settings.SAML_ENABLED:
    urlpatterns += [
        path('reset/', PasswordResetView.as_view(),
            {
                'post_reset_redirect': '/account/reset/done/',
                'template_name': 'password_reset.html'
            },
            name="password_reset"
        ),

        path('reset/done/', PasswordChangeDoneView.as_view(), {
            'template_name': 'password_reset_done.html'},
            name="password_reset_done"
        ),

        re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), {
            'post_reset_redirect': '/',
            'template_name': 'password_reset_confirm.html'},
            name="password_reset_confirm"
        ),

        path('changepass/', rattic_change_password, {
            'post_change_redirect': '/account/',
            'template_name': 'account_changepass.html'}, name='password_change')
    ]

# URLs we do want enabled with LDAP
if settings.LDAP_ENABLED and settings.AUTH_LDAP_ALLOW_PASSWORD_CHANGE and not settings.SAML_ENABLED:
    urlpatterns += [
        path('changepass/', ldap_password_change, {}, name='password_change')
    ]