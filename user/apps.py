from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"

    # https://docs.djangoproject.com/en/6.1/ref/applications/#django.apps.AppConfig.ready
    def ready(self):
        import user.signals  # noqa: F401
