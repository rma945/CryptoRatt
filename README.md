Description
============

**Project archived**

RatticWeb is the website part of the Rattic password management solution, which allows you to easily manage your users and passwords.

If you decide to use RatticWeb you should take the following into account:
* The webpage should be served over HTTPS only, apart from a redirect from normal HTTP.
* The filesystem in which the database is stored should be protected with encryption.
* The access logs should be protected.
* The machine which serves RatticWeb should be protected from access.
* Tools like [OSSEC](http://www.ossec.net/) are your friend.



This fork change
=================

* add SAML2 based auth
* add JS based copy button
* add per-user based access to credentials
* fix staff access to not owned credentials
* add multi-staff groups support

TODO:
=====
replace django-database-files==0.1 replace with BinaryField
replace keepassdb
replace tastypie
add language support to user profile