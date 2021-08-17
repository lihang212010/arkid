from ..views.sdk import SdkView
from django.urls import path

urlpatterns = [
    path('sdk/', SdkView.as_view()),
]