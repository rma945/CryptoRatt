# CryptoRatt

CryptoRatt - is a credentials managment solution, that aimed for provide a free and useful password management solution for small or large teams. It provides SSO login via LDAP or ID, and password management audit, permissions managment and more. This project was  forked from [tildashas/RatticWeb](https://github.com/tildaslash/RatticWeb) with additional features and updated UI.

## Features

* SSO login throught OIDC or LDAP
* Permission managment for credentials
* Project based credentials managment
* Multiple attachments per credential
* Password generator with password strong meter
* Credential icons

## Screenshots

Credential view page

![Credential password generator](https://raw.githubusercontent.com/rma945/CryptoRatt/media/images/screenshot-2.png)

Credential edit page

![Credential edit page](https://raw.githubusercontent.com/rma945/CryptoRatt/media/images/screenshot-0.png)

Credential password generator

![Credential password generator](https://raw.githubusercontent.com/rma945/CryptoRatt/media/images/screenshot-1.png)

Credential list

![Credential list](https://raw.githubusercontent.com/rma945/CryptoRatt/media/images/screenshot-3.png)

## Installation

### Requirements

* Python >= 3.6
* MySQL or MariaDB >= 5.6

### Installlation

Clone project repository

```bash
mkdir -p /opt/cryptoratt/
cd /opt/cryptoratt/
git clone https://github.com/rma945/CryptoRatt ./
```

Setup virtual environment for project

```bash
pip3 install virtualenv
virtualenv .env
. .env/bin/activate
pip3 install -r requirements/requirements-mysql.txt
```

Create uwsgi configuration

```bash
cat << EOF > /etc/uwsgi.d/cryptoratt.ini
[uwsgi]
uid          = nginx
gid          = nginx
http-socket  = 127.0.0.1:8081
chdir        = /opt/cryptoratt
home         = /opt/cryptoratt/.env/
plugins      = python36
module       = apps.ratticweb.wsgi
master       = true
workers      = 2
max-requests = 1024
harakiri     = 30
die-on-term  = true
EOF
```

Create nginx virtual host

```bash
cat << EOF > /etc/nginx/conf.d/cryptoratt.example.com.conf
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name cryptoratt.example.com;

    access_log /var/log/nginx/cryptoratt.example.com-access.log;
    error_log /var/log/nginx/cryptoratt.example.com.log error;

    ssl_certificate     /etc/ssl/_.example.com.crt;
    ssl_certificate_key /etc/ssl/_.example.com.key;
    ssl_protocols       TLSv1.2;
    ssl_session_cache   shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';
    ssl_prefer_server_ciphers on;
    add_header Strict-Transport-Security max-age=15768000;

    location /static/ {
      root /opt/cryptoratt/;
      access_log off;
      expires max;
    }

    location / {
      proxy_pass http://127.0.0.1:8081;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   }
}
EOF
```

Collect static files

```bash
./manage.py collectstatic
```

Run database migrations

```bash
./manage.py migrate
```

## How to migrate from Rattic 1.3.1

If you planning to migrate from Rattic v1.3.1, you need to create new virtual environment with python >= 3.6 and update your MySQL to >=5.6

Then, backup your database and perform this migrations for update database scheme and migrate attachments to new storage model:

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
./manage.py migrate cred 0001_initial --fake
./manage.py migrate cred 0002_add_projects
./manage.py migrate cred 0003_upgrade_to_django22 -v 3
./manage.py migrate account 0001_initial --fake
./manage.py migrate account 0002_upgrade_to_django22
./manage.py migrate account 0003_upgrade_to_boostrap
./manage.py migrate cred 0004_upgrade_to_boostrap
./manage.py migrate cred 0005_credential_icons
./manage.py migrate
```
