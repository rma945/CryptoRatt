from django.urls import path
from django.conf import settings
from apps.staff.views import *

app_name = "staff"
urlpatterns = [
    # Views in views.py
    path('', home, name="home"),

    # User/Group Management
    path('userdetail/<int:uid>/', userdetail, name="user_detail"),
    path('removetoken/<int:uid>/', removetoken, name="remove_token"),
    path('groupdetail/<int:gid>/', groupdetail, name="group_detail"),

    # Auditing
    path('audit-by-<slug:by>/<int:byarg>/', audit, name="audit"),

    # Importing
    path('import/keepass/', upload_keepass),
    path('import/process/', import_overview),
    path('import/process/<int:import_id>/', import_process),
    path('import/process/<int:import_id>/ignore/', import_ignore),

    # credentials undeletion
    path('credundelete/<int:cred_id>/', credundelete, name="cred_undelete"),

    # group \ user delete
    path('useredit/<int:pk>/', UpdateUser.as_view(), name="user_edit"),
    path('groupdelete/<int:gid>/', groupdelete, name="group_delete"),
    path('userdelete/<int:uid>/', userdelete, name="user_delete"),
]


# don`t manage groups if USE_LDAP_GROUPS or SAML_ENABLED
if (not settings.USE_LDAP_GROUPS and not settings.SAML_ENABLED):
    urlpatterns += [
        # Group Management
        path('groupadd/', groupadd, name="group_add"),
        path('groupedit/<int:gid>/', groupedit, name="group_edit"),
    ]

# don`t add users if USE_LDAP_GROUPS or SAML_ENABLED
if (not settings.LDAP_ENABLED and not settings.SAML_ENABLED):
    urlpatterns += [
        # staff.views,
        # User Management
        path('useradd/', NewUser.as_view(), name="user_add"),
    ]
