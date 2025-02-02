from django.apps import AppConfig


class UserModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_module'
    verbose_name = 'Users'

    def ready(self):
        import user_module.signals
