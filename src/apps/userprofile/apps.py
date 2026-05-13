from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = 'apps.userprofile'

    def ready(self):
        import apps.userprofile.signals  # noqa: F401
