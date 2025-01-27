from django.urls import path
from .views import (PostAPIView,
                    PostDetailAPIView)

urlpatterns = [
    path('', PostAPIView.as_view(), name='posts'),
    path('<str:post_id>', PostDetailAPIView.as_view(), name='post-detail'),
]
