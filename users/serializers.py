from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Для отображения и создания объектов платежей."""

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Для создания платежа.

    Используется при POST-запросах для создания объекта Payment.
    Позволяет указать оплату либо за курс, либо за отдельный урок.

    Правила валидации:
    - необходимо указать либо paid_course, либо paid_lesson;
    - нельзя указывать paid_course и paid_lesson одновременно.
    """

    class Meta:
        model = Payment
        fields = ("paid_course", "paid_lesson", "amount", "payment_method")

    def validate(self, attrs):
        paid_course = attrs.get("paid_course")
        paid_lesson = attrs.get("paid_lesson")

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError(
                "Нужно указать paid_course или paid_lesson."
            )
        if paid_course and paid_lesson:
            raise serializers.ValidationError(
                "Нельзя одновременно paid_course и paid_lesson."
            )

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Для просмотра и редактирования пользователя (без пароля)."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar']


class UserCreateSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'city', 'avatar']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
