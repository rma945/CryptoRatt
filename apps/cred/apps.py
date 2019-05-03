from django.apps import AppConfig

class AppConfig(AppConfig):
    name = "apps.cred"

    def ready(self):
      import apps.account.signals
