from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    Полный CRUD для Course через ViewSet:
    - list (GET /courses/)
    - retrieve (GET /courses/{id}/)
    - create (POST /courses/)
    - update/partial_update (PUT/PATCH /courses/{id}/)
    - destroy (DELETE /courses/{id}/)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        elif self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]
        return [p() for p in permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /lessons/  — список уроков
    POST /lessons/ — создание урока
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /lessons/{id}/ — получить урок
    PUT    /lessons/{id}/ — полное обновление
    PATCH  /lessons/{id}/ — частичное обновление
    DELETE /lessons/{id}/ — удалить
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]
        return [p() for p in permission_classes]
