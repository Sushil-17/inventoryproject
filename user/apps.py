from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'


# problem percievs in the below block for admin login.
    # def ready(self):
    #     import user.signals
