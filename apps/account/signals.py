import urllib
from hashlib import md5
from base64 import b64encode

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in

from apps.account.models import UserProfile

def CreateUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def GetUserGravatar(sender, user, request, **kwargs):
    user_profile = UserProfile.objects.get(user=user)

    if user.email and not user_profile.avatar:
        gravatar_base_url = 'https://www.gravatar.com/avatar/'
        options = urllib.parse.urlencode({'size': 160, 'default': 404})
        email = md5(user.email.encode('utf-8')).hexdigest()
        gravatar_url = gravatar_base_url + email + '?' + options

        # download gravatar if it exists and update user profile
        try:
            gravatar_req_data = urllib.request.urlopen(gravatar_url).read()
            user_profile.avatar = b64encode(gravatar_req_data)
            user_profile.save()

        except urllib.error.HTTPError:
            return



# add signal for create user profile after login
post_save.connect(CreateUserProfile, sender=User)

# add signal for a get Gravatar for user
user_logged_in.connect(GetUserGravatar)
