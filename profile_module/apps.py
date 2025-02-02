from django.apps import AppConfig


class AccountModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_module'

    def ready(self):
        import profile_module.signals
