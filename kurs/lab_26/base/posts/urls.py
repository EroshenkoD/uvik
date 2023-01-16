from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'set_posts', views.PostsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('class_posts/', views.PostsList.as_view()),
    path('class_posts/<int:likes>/', views.PostsList.as_view()),
    path('def_posts/<int:pk>/', views.post_detail),
]