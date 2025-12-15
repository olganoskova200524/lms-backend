from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from users.permissions import IsNotModeratorForCreateDelete
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

    def get_permissions(self):
        """
        Модератор:
          - может смотреть список и детали курса (GET)
          - может редактировать (PUT/PATCH)
          - не может создавать и удалять (POST/DELETE)
        Остальные аутентифицированные пользователи — без ограничений.
        """
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsNotModeratorForCreateDelete]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /lessons/  — список уроков
    POST /lessons/ — создание урока
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModeratorForCreateDelete]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /lessons/{id}/ — получить урок
    PUT    /lessons/{id}/ — полное обновление
    PATCH  /lessons/{id}/ — частичное обновление
    DELETE /lessons/{id}/ — удалить
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModeratorForCreateDelete]
