from django.urls import path
from rest_framework.authtoken import views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserCreateView

urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('api/token/', views.obtain_auth_token)

    # path('token/', TokenObtainPairView.as_view()),
    # path('token/refresh/', TokenRefreshView.as_view()),
]