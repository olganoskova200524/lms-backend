from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Для отображения и создания объектов платежей."""

    class Meta:
        model = Payment
        fields = '__all__'


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
