from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 디렉토리 변경에 의한 변경
    name = 'api.users'
