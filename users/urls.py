from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from viva.apps import VivaConfig
from users.views import RegisterView, password_reset_view,activate

#from users.views import

app_name = VivaConfig.name
urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_request/', password_reset_view, name='password_request'),
]
