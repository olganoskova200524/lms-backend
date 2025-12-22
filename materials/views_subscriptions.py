from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Course, Subscription


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Подписка на курс (toggle)",
        description=(
                "Если подписка на курс уже существует — удаляет её.\n"
                "Если подписки нет — создаёт."
        ),
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "course_id": {"type": "integer", "example": 1},
                },
                "required": ["course_id"],
            }
        },
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "подписка добавлена"},
                        "is_subscribed": {"type": "boolean", "example": True},
                    },
                },
                description="Статус подписки после выполнения операции",
            ),
            404: OpenApiResponse(description="Курс не найден"),
        },
        tags=["Subscriptions"],
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_qs = Subscription.objects.filter(user=user, course=course_item)

        if subs_qs.exists():
            subs_qs.delete()
            message = "подписка удалена"
            is_subscribed = False
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
            is_subscribed = True

        return Response({"message": message, "is_subscribed": is_subscribed})
