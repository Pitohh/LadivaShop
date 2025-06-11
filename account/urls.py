from django.urls import path
from .views import RegisterView, UserProfileView, LoginView, user_logout

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('login/', LoginView, name='login'),
    path('logout/', user_logout, name='logout'),
]
