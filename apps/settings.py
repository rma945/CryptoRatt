#########################
# Do not edit this file #
#########################

from configparser import RawConfigParser, NoOptionError
from urllib.parse import urljoin
import ldap
import os
from django_auth_ldap.config import LDAPSearch
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

import uuid
uuid._uuid_generate_random = None

config = RawConfigParser()
config.read_file(open('conf/defaults.cfg'))
CONFIGURED_BY = config.read(['conf/local.cfg'])

def confget(section, var, default):
    try:
        return config.get(section, var)
    except NoOptionError:
        return default

def confgetbool(section, var, default):
    try:
        return config.getboolean(section, var)
    except NoOptionError:
        return default

# debug settings
DEBUG = confgetbool('ratticweb', 'debug', False)

# the Internationalization Settings
USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    'apps/locale',
)

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in locations
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE = (
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # Custom Middleware
    'django_otp.middleware.OTPMiddleware',
    'apps.account.middleware.StrictAuthentication',
    'apps.account.middleware.PasswordExpirer',
    'apps.ratticweb.middleware.DisableClientSideCachingMiddleware',
    'apps.ratticweb.middleware.XUACompatibleMiddleware',
    'apps.ratticweb.middleware.CSPMiddleware',
    'apps.ratticweb.middleware.HSTSMiddleware',
    'apps.ratticweb.middleware.DisableContentTypeSniffing',
)

ROOT_URLCONF = 'apps.ratticweb.urls'

# Urls
RATTIC_ROOT_URL = '/'
MEDIA_URL = urljoin(RATTIC_ROOT_URL, 'media/')
STATIC_URL = urljoin(RATTIC_ROOT_URL, 'static/')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'apps.ratticweb.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/templates',
            '/templates/events'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                'apps.ratticweb.context_processors.base_template_reqs',
                'apps.ratticweb.context_processors.logo_selector',
            ],
        },
    },
]

LOCAL_APPS = (
    'apps.ratticweb',
    'apps.cred',
    'apps.account',
    'apps.staff',
    'apps.help',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'user_sessions',
    'django_saml2_auth',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'tastypie',
) + LOCAL_APPS

if os.environ.get("ENABLE_TESTS") == "1":
    INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'tests.runner.ExcludeAppsTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format'
        }
    },
    'loggers': {
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
        },
        'db_backup': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

#######################
# Custom app settings #
#######################

# URLs
PUBLIC_HELP_WIKI_BASE = 'https://github.com/rma945/CryptoRatt/wiki/'
LOGIN_REDIRECT_URL = urljoin(RATTIC_ROOT_URL, "cred/list/")
LOGOUT_REDIRECT_URL = urljoin(RATTIC_ROOT_URL, "/")
LOGIN_URL = RATTIC_ROOT_URL

# django-user-sessions
SESSION_ENGINE = 'user_sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = int(config.get('ratticweb', 'session_cookie_age'))

# django-auth-ldap
AUTH_LDAP_USER_FLAGS_BY_GROUP = {}

###############################
# External environment config #
###############################

# [ratticweb]
TIME_ZONE = config.get('ratticweb', 'timezone')
SECRET_KEY = config.get('ratticweb', 'secretkey')
HOSTNAME = config.get('ratticweb', 'hostname')
RATTIC_MAX_ATTACHMENTS = int(config.get('ratticweb', 'max_attachments'))
RATTIC_MAX_ATTACHMENT_SIZE = int(config.get('ratticweb', 'max_attachment_size'))

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS += config.get('ratticweb', 'hostname'), 'localhost'

# Allow SSL termination outside RatticDB
if confget('ratticweb', 'ssl_header', False):
    SECURE_PROXY_SSL_HEADER = (config.get('ratticweb', 'ssl_header'), config.get('ratticweb', 'ssl_header_value'))

# Setup the loglevel
LOGGING['loggers']['django.request']['level'] = config.get('ratticweb', 'loglevel')

# [filepaths]
HELP_SYSTEM_FILES = confget('filepaths', 'help', False)
MEDIA_ROOT = confget('filepaths', 'media', '')
STATIC_ROOT = confget('filepaths', 'static', '')

# [database]
DATABASES = {
    'default': {
        'ENGINE': confget('database', 'engine', 'django.db.backends.sqlite3'),
        'NAME': confget('database', 'name', 'db/ratticweb'),
        'USER': confget('database', 'user', ''),
        'PASSWORD': confget('database', 'password', ''),
        'HOST': confget('database', 'host', ''),
        'PORT': confget('database', 'port', ''),
    }
}

# [backup]
BACKUP_DIR = confget("backup", "dir", None)
BACKUP_GPG_HOME = confget("backup", "gpg_home", None)
BACKUP_S3_BUCKET = confget("backup", "s3_bucket", None)
BACKUP_RECIPIENTS = confget("backup", "recipients", None)

# [email]
# SMTP Mail Opts
EMAIL_BACKEND = config.get('email', 'backend')
EMAIL_FILE_PATH = config.get('email', 'filepath')
EMAIL_HOST = config.get('email', 'host')
EMAIL_PORT = config.get('email', 'port')
EMAIL_HOST_USER = config.get('email', 'user')
EMAIL_HOST_PASSWORD = config.get('email', 'password')
EMAIL_USE_TLS = confgetbool('email', 'usetls', False)
DEFAULT_FROM_EMAIL = config.get('email', 'from_email')

# [saml]
SAML_ENABLED = 'saml' in config.sections()

if SAML_ENABLED:
    # SAML IDP URL
    SAML_IDP_URL = config.get('saml', 'idp_url')
    
    # SAML
    SAML2_AUTH = {
        # Metadata is required, choose either remote url or local file path
        'ENTITY_ID': confget('saml', 'entity_id', ''),
        'METADATA_AUTO_CONF_URL': confget('saml', 'metadata_url', ''),
        'NAME_ID_FORMAT': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',

        # Optional settings below
        'DEFAULT_NEXT_URL': '/cred/list/',
        'CREATE_USER': 'TRUE',
        'NEW_USER_PROFILE': {
            'ACTIVE_STATUS': True,
            'STAFF_STATUS': False,
            'SUPERUSER_STATUS': False,
        },
        'ATTRIBUTES_MAP': {
            'email': confget('saml', 'attribute_email', 'email'),
            'username': confget('saml', 'attribute_username', 'username'),
            'first_name': confget('saml', 'attribute_firstname', 'firstname'),
            'last_name': confget('saml', 'attribute_lastname', 'lastname'),
        },
            'TRIGGER': {
            'BEFORE_LOGIN': 'apps.ratticweb.saml.hooks.sync_user',
        },
    }

# [ldap]
LDAP_ENABLED = 'ldap' in config.sections()

if LDAP_ENABLED:

    LOGGING['loggers']['django_auth_ldap']['level'] = confget('ldap', 'loglevel', 'WARNING')

    # Needed if anonymous queries are not allowed
    AUTH_LDAP_BIND_DN = confget('ldap', 'binddn', '')

    AUTH_LDAP_BIND_PASSWORD = confget('ldap', 'bindpw', '')

    # User attributes
    AUTH_LDAP_USER_ATTR_MAP = {"email": "mail"}
    if config.has_option('ldap', 'userfirstname'):
        AUTH_LDAP_USER_ATTR_MAP["first_name"] = config.get('ldap', 'userfirstname')
    if config.has_option('ldap', 'userfirstname'):
        AUTH_LDAP_USER_ATTR_MAP["last_name"] = config.get('ldap', 'userlastname')

    # Are we using LDAP groups or local groups? Default to using LDAP groups
    USE_LDAP_GROUPS = confgetbool('ldap', 'useldapgroups', True)

    # If we are not using LDAP groups, then do not update the user model's group membership
    AUTH_LDAP_MIRROR_GROUPS = USE_LDAP_GROUPS

    AUTH_LDAP_SERVER_URI = config.get('ldap', 'uri')

    AUTH_LDAP_USER_BASE = config.get('ldap', 'userbase')

    # Defaults to AUTH_LDAP_USER_BASE because it must be defined
    AUTH_LDAP_GROUP_BASE = confget('ldap', 'groupbase', AUTH_LDAP_USER_BASE)

    AUTH_LDAP_USER_FILTER = config.get('ldap', 'userfilter')

    # Defaults to a bogus filter so that searching yields no errors in the log
    AUTH_LDAP_GROUP_FILTER = confget('ldap', 'groupfilter', '(objectClass=_fake)')

    AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USER_BASE, ldap.SCOPE_SUBTREE,
                                       AUTH_LDAP_USER_FILTER)

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_GROUP_BASE, ldap.SCOPE_SUBTREE,
                                        AUTH_LDAP_GROUP_FILTER)

    # Defaults to PosixGroupType because it must match a pre-defined list of selections
    AUTH_LDAP_GROUP_TYPE = getattr(__import__('django_auth_ldap').config, confget('ldap', 'grouptype', 'PosixGroupType'))()

    # Booleans
    AUTH_LDAP_ALLOW_PASSWORD_CHANGE = confgetbool('ldap', 'pwchange', False)

    AUTH_LDAP_START_TLS = confgetbool('ldap', 'starttls', False)

    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: confgetbool('ldap', 'requirecert', True),
        ldap.OPT_REFERRALS: confgetbool('ldap', 'referrals', False),
    }

    # Determines which LDAP users are staff, if not defined, privilege can be set manually
    if config.has_option('ldap', 'staff'):
        AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = confget('ldap', 'staff', '')

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
else:
    # No LDAP section means no LDAP groups
    USE_LDAP_GROUPS = False

# Passwords expiry settings
if LDAP_ENABLED or SAML_ENABLED:
    PASSWORD_EXPIRY = False
else:
    try:
        PASSWORD_EXPIRY = timedelta(days=int(config.get('ratticweb', 'passwordexpirydays')))
    except NoOptionError:
        PASSWORD_EXPIRY = False
    except ValueError:
        PASSWORD_EXPIRY = False
