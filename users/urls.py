from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-account-details/', views.edit_account_details, name='edit-account-details'),
    path('logout/', views.logout_view, name='logout'),
]

