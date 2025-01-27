from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 디렉토리 구조 변경에 의한 변경
    name = 'api.posts'
