from django.urls import path

from .views import SignupView, UserLoginView, UserLogoutView

urlpatterns = [
    path('inscription/', SignupView.as_view(), name='signup'),
    path('connexion/', UserLoginView.as_view(), name='login'),
    path('deconnexion/', UserLogoutView.as_view(), name='logout'),
]
