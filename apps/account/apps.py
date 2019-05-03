from django.apps import AppConfig

class AppConfig(AppConfig):
    name = "apps.account"

    def ready(self):
      import apps.account.signals
