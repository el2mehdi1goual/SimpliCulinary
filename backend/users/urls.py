from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('inscription/', SignUpView.as_view(), name='signup'),
]
