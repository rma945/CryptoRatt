from django.urls import path
from django.conf import settings
from apps.staff.views import *

app_name = "staff"
urlpatterns = [
    path('', app_settings, name="settings"),
    path('users/', users, name="users"),
    path('groups/', groups, name="groups"),
    path('tags/', tags, name="tags"),
    # path('trash/', trash, name="trash"),

    # User/Group Management
    path('user/<int:uid>/', user_detail, name="user_detail"),  
    path('group/<int:gid>/', group_detail, name="group_detail"),

    # audit
    path('audit-by-<slug:by>/<int:byarg>/', audit, name="audit"),

    # credentials undeletion
    path('credundelete/<int:cred_id>/', credundelete, name="cred_undelete"),

    # group \ user delete
    path('edit/user/<int:uid>/', edit_user, name="edit_user"),
    path('edit/group/<int:gid>/', edit_group, name="edit_group"),
    path('delete/group/<int:gid>/', delete_group, name="delete_group"),
    path('delete/user/<int:uid>/', delete_user, name="delete_user"),

    # api
    path('deactivate/user/', deactivate_user, name="deactivate_user"),
    # path('delete/token/<int:uid>/', delete_token, name="delete_token"),
]

# disable adduser if LDAP or SAML enabled
if (not settings.LDAP_ENABLED and not settings.SAML_ENABLED):
    urlpatterns += [
        path('groupadd/', groupadd, name="group_add"),
        path('useradd/', NewUser.as_view(), name="user_add"),
    ]
