# Description

RatticWeb is the website part of the Rattic password management solution, which allows you to easily manage your users and passwords.

If you decide to use RatticWeb you should take the following into account:
* The webpage should be served over HTTPS only, apart from a redirect from normal HTTP.
* The filesystem in which the database is stored should be protected with encryption.
* The access logs should be protected.
* The machine which serves RatticWeb should be protected from access.
* Tools like [OSSEC](http://www.ossec.net/) are your friend.

# Changes

* added SAML2 based auth
* added JS based copy button
* added per-user based access to credentials
* fixed staff access to not owned credentials
* added multi-staff groups support
* added projects
* added multiple attachments field

# How to migrate from Rattic 1.3.1 

#### Update python modules

```
pip3 install -U -r requirements-mysql.txt
```

#### system migrations
```bash
./manage.py migrate contenttypes 0001_initial --fake
./manage.py migrate contenttypes 0002_remove_content_type_name
./manage.py migrate otp_static --fake
./manage.py migrate otp_totp --fake
./manage.py migrate sessions --fake
./manage.py migrate tastypie 0001_initial --fake
./manage.py migrate tastypie 0002_api_access_url_length
./manage.py migrate two_factor 0001_initial --fake
./manage.py migrate two_factor 0002_auto_20150110_0810
./manage.py migrate two_factor 0003_auto_20150817_1733
./manage.py migrate two_factor 0004_auto_20160205_1827
./manage.py migrate two_factor 0005_auto_20160224_0450
./manage.py migrate user_sessions 0001_initial --fake
./manage.py migrate user_sessions 0002_auto_20151208_1536
./manage.py migrate user_sessions 0003_auto_20161205_1516
./manage.py migrate auth 0002_alter_permission_name_max_length
./manage.py migrate auth 0003_alter_user_email_max_length
./manage.py migrate auth 0004_alter_user_username_opts
./manage.py migrate auth 0005_alter_user_last_login_null
./manage.py migrate auth 0006_require_contenttypes_0002
./manage.py migrate auth 0007_alter_validators_add_error_messages
./manage.py migrate auth 0008_alter_user_username_max_length
./manage.py migrate auth 0009_alter_user_last_name_max_length
./manage.py migrate auth 0010_alter_group_name_max_length
./manage.py migrate auth 0011_update_proxy_permissions
./manage.py migrate admin 0001_initial --fake
./manage.py migrate admin 0002_logentry_remove_auto_add
./manage.py migrate admin 0003_logentry_add_action_flag_choices
```
#### app migrations
```bash
./manage.py migrate cred 0001_initial --fake
./manage.py migrate cred 0002_add_projects
./manage.py migrate cred 0003_upgrade_to_django22 -v 3
./manage.py migrate account 0001_initial --fake
./manage.py migrate account 0002_upgrade_to_django22
```