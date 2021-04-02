from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path("gitee/login", views.GiteeLoginView.as_view(), name="login"),
    path("gitee/callback", views.GiteeCallbackView.as_view(), name="callback"),
    path("gitee/bind", views.GiteeBindAPIView.as_view(), name="bind"),
    # path(
    #     "gitee/register/bind",
    #     views.GiteeRegisterAndBindView.as_view(),
    #     name="register_bind",
    # ),
]