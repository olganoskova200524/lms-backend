from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, UserRegisterAPIView, PaymentListAPIView, PaymentCreateAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('users/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
