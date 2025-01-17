from django.urls import path
from . import views


urlpatterns = [
    path('github/login', views.GithubLoginView.as_view(), name='login'),
    path('github/callback', views.GithubCallbackView.as_view(), name='callback'),
    path('github/bind', views.GithubBindAPIView.as_view(), name='bind'),
    path('github/unbind', views.GithubUnBindView.as_view(), name='unbind'),
    # path('github/register/bind', views.GithubRegisterAndBindView.as_view(), name='register_bind'),
]
