from rest_framework.permissions import BasePermission

MODERATOR_GROUP_NAME = 'moderators'


class IsModerator(BasePermission):
    """
    True, если пользователь состоит в группе модераторов.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
        )


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
