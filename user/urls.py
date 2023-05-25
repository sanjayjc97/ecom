from django.urls import path
from .views import *

urlpatterns = [
    path('',Login_signup_view.as_view(method_name = 'login_view'),name = 'login'),
    path('logout',Login_signup_view.as_view(method_name = 'logout_view'),name = 'logout'),
    path('signup',Login_signup_view.as_view(method_name = 'signup_view'),name = 'signup')
]