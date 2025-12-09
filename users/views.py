from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    """
    GET /api/payments/

    Фильтры:
      ?paid_course=<id>
      ?paid_lesson=<id>
      ?payment_method=cash|transfer

    Сортировка по дате:
      ?ordering=payment_date      (по возрастанию)
      ?ordering=-payment_date     (по убыванию)
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
