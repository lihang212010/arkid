from django.conf.urls import url
from django.urls import re_path
from oauth2_provider import views
from .views import AuthorizationView


base_urlpatterns = [
    url(r"oauth/authorize/$", AuthorizationView.as_view(), name="authorize"),
    url(r"oauth/token/$", views.TokenView.as_view(), name="token"),
    url(r"oauth/revoke_token/$", views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r"oauth/introspect/$", views.IntrospectTokenView.as_view(), name="introspect"),
]

oidc_urlpatterns = [
    url(r".well-known/openid-configuration/$", views.ConnectDiscoveryInfoView.as_view(), name="oidc-connect-discovery-info",),
    url(r"oauth/userinfo/$", views.UserInfoExtendView.as_view(), name="oauth-user-info"),
    url(r"oidc/logout/$", views.OIDCLogoutView.as_view(), name="oauth-user-logout"),
    re_path(r".well-known/jwks.json$", views.JwksInfoView.as_view(), name="jwks-info"),
    re_path(r"userinfo/$", views.UserInfoView.as_view(), name="user-info"),
]

urlpatterns = base_urlpatterns + oidc_urlpatterns