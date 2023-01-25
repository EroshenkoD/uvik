from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls), name='users_set'),
    path('posts/', views.PostListView.as_view(), name='posts_view'),
    path('posts/<int:pk>/', views.PostUpdateView.as_view(), name='posts_update'),
    path('posts_delete/<int:pk>/', views.PostDeleteView.as_view(), name='posts_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
