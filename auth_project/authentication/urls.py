from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, UserDetailsView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('register/verify/', VerifyOTPView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', UserDetailsView.as_view()),
    path('logout/', LogoutView.as_view()),
]
