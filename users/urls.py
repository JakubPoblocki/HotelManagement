from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
    path('login/', views.login_user, name='login'),
    path('get-csrf-token/', views.get_csrf_token_view, name='get_csrf_token')
]