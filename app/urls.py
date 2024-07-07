from django.urls import path
from .views import register_user, user_login,upload_csv,get_data

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('upload/',upload_csv,name='upload_csv'),
    path('get_data/', get_data, name='get_data')
]