from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<category>/", views.category, name="category"),
]