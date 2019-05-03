import urllib
from hashlib import md5
from base64 import b64encode
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

from apps.account.models import UserProfile


def GetUserGravatar(sender, user, request, **kwargs):
    user_profile = UserProfile.objects.get(user=user)

    if user.email and not user_profile.avatar:
        gravatar_base_url = 'https://www.gravatar.com/avatar/'
        options = urllib.parse.urlencode({'size': 160})
        email = md5(user.email.encode('utf-8')).hexdigest()

        gravatar_url = gravatar_base_url + email + options

        # download gravatar and add it to user avatar
        avatar_data = urllib.request.urlopen(gravatar_url).read()
        user_profile.avatar = b64encode(avatar_data)
        user_profile.save()

user_logged_in.connect(GetUserGravatar)
