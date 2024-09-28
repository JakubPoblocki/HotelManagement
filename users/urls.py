from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
]