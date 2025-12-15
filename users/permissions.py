from rest_framework.permissions import BasePermission

MODERATOR_GROUP_NAME = 'moderators'


class IsModerator(BasePermission):
    """
    True, если пользователь состоит в группе модераторов.
    """

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.is_authenticated
                and request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    True, если пользователь является владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and getattr(obj, "owner_id", None) == request.user.id


class IsNotModeratorForCreateDelete(BasePermission):
    """
    Запрещает модераторам создавать и удалять объекты.

    - Для методов POST/DELETE возвращает False, если пользователь модератор.
    - Для остальных методов (GET, PUT, PATCH и т.п.) даёт проход.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        is_moderator = user.groups.filter(name=MODERATOR_GROUP_NAME).exists()

        if request.method in ('POST', 'DELETE'):
            return not is_moderator
        return True
