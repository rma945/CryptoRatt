from django.urls import path
from django.conf import settings
from apps.staff.views import *

app_name = "staff"
urlpatterns = [
    path('', app_settings, name="settings"),
    path('users/', users, name="users"),
    path('groups/', groups, name="groups"),
    path('tags/', tags, name="tags"),

    # User/Group Management
    path('user/<int:uid>/', userdetail, name="user_detail"),
    path('removetoken/<int:uid>/', removetoken, name="remove_token"),
    path('groupdetail/<int:gid>/', groupdetail, name="group_detail"),

    # Auditing
    path('audit-by-<slug:by>/<int:byarg>/', audit, name="audit"),

    # credentials undeletion
    path('credundelete/<int:cred_id>/', credundelete, name="cred_undelete"),

    # group \ user delete
    path('edit/user/<int:pk>/', UpdateUser.as_view(), name="edit_user"),
    path('delete/group/<int:gid>/', delete_group, name="delete_group"),
    path('delete/user/<int:uid>/', delete_user, name="delete_user"),
]

# disable addgroup if LDAP or SAML enabled
if (not settings.USE_LDAP_GROUPS and not settings.SAML_ENABLED):
    urlpatterns += [
        # Group Management
        path('groupadd/', groupadd, name="group_add"),
        path('groupedit/<int:gid>/', groupedit, name="group_edit"),
    ]

# disable adduser if LDAP or SAML enabled
if (not settings.LDAP_ENABLED and not settings.SAML_ENABLED):
    urlpatterns += [
        path('useradd/', NewUser.as_view(), name="user_add"),
    ]
