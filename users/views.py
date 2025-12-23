from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import (
    PaymentSerializer,
    UserSerializer,
    UserCreateSerializer, PaymentCreateSerializer
)
from .services.stripe import create_stripe_product, create_stripe_price, create_stripe_checkout_session

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
    Список платежей с фильтрацией и сортировкой по дате.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Создаёт платёж и Stripe Checkout Session, возвращая ссылку на оплату.
    """
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment: Payment = serializer.save(user=request.user)

        target = payment.paid_course or payment.paid_lesson
        product_name = getattr(target, "title", "Оплата")
        product_description = getattr(target, "description", "")

        product = create_stripe_product(name=product_name, description=product_description)
        price = create_stripe_price(product_id=product.id, amount=payment.amount)
        session = create_stripe_checkout_session(price_id=price.id)

        payment.stripe_product_id = product.id
        payment.stripe_price_id = price.id
        payment.stripe_session_id = session.id
        payment.payment_url = session.url
        payment.save(update_fields=[
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
        ])

        return Response(
            {
                "id": payment.id,
                "payment_url": payment.payment_url,
                "stripe_session_id": payment.stripe_session_id,
            },
            status=status.HTTP_201_CREATED,
        )
