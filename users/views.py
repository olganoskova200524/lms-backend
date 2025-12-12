from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import OrderingFilter

from .models import Payment
from .serializers import (
    PaymentSerializer,
    UserSerializer,
    UserCreateSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Полный CRUD по пользователям.
    Доступ ограничен правами IsAuthenticated (из settings.py).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступ открытый (AllowAny).
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class PaymentListAPIView(generics.ListAPIView):
    """
    GET /api/payments/

    Фильтры:
      ?paid_course=<id>
      ?paid_lesson=<id>
      ?payment_method=cash|transfer

    Сортировка:
      ?ordering=payment_date
      ?ordering=-payment_date
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
