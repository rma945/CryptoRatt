from django.apps import AppConfig
from django.contrib.auth import get_user_model

class AppConfig(AppConfig):
    name = "apps.account"

    def ready(self):
      # inport user login signals
      import apps.account.signals
      
      # extends user model with 2fa status check method
      from apps.account.models import is_2fa_enabled
      UserModel = get_user_model()
      UserModel.add_to_class('is_2fa_enabled', is_2fa_enabled)
