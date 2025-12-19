from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="owner@test.com", password="12345")
        self.other = User.objects.create_user(email="other@test.com", password="12345")

        self.moderator = User.objects.create_user(email="mod@test.com", password="12345")
        moderators_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            title="Курс владельца",
            description="desc",
            owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Урок 1",
            description="desc",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.owner
        )

        self.lesson_list_url = reverse("lesson-list-create")
        self.lesson_detail_url = lambda pk: reverse("lesson-detail", args=[pk])

    def test_owner_can_create_lesson_with_youtube_url(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            "course": self.course.id,
            "title": "Новый урок",
            "description": "text",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        resp = self.client.post(self.lesson_list_url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title="Новый урок", owner=self.owner).exists())

    def test_owner_cannot_create_lesson_with_non_youtube_url(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            "course": self.course.id,
            "title": "Плохая ссылка",
            "description": "text",
            "video_url": "https://stepik.org/course/123",
        }
        resp = self.client.post(self.lesson_list_url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", resp.data)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        data = {
            "course": self.course.id,
            "title": "Модер создаёт",
            "description": "text",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        resp = self.client.post(self.lesson_list_url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_lesson(self):
        self.client.force_authenticate(user=self.owner)

        data = {"title": "Урок 1 обновлён"}
        resp = self.client.patch(self.lesson_detail_url(self.lesson.id), data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Урок 1 обновлён")

    def test_other_user_cannot_update_lesson(self):
        self.client.force_authenticate(user=self.other)

        data = {"title": "Пытаюсь обновить"}
        resp = self.client.patch(self.lesson_detail_url(self.lesson.id), data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        data = {"title": "Модератор обновил"}
        resp = self.client.patch(self.lesson_detail_url(self.lesson.id), data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)

        resp = self.client.delete(self.lesson_detail_url(self.lesson.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        resp = self.client.delete(self.lesson_detail_url(self.lesson.id))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_lessons_list_filtered_for_non_moderator(self):
        self.client.force_authenticate(user=self.owner)
        resp_owner = self.client.get(self.lesson_list_url)
        self.assertEqual(resp_owner.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_owner.data["count"], 1)

        self.client.force_authenticate(user=self.other)
        resp_other = self.client.get(self.lesson_list_url)
        self.assertEqual(resp_other.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_other.data["count"], 0)

    def test_lessons_list_for_moderator_shows_all(self):
        self.client.force_authenticate(user=self.moderator)
        resp = self.client.get(self.lesson_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="12345")
        self.moderator = User.objects.create_user(email="mod2@test.com", password="12345")
        moderators_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            title="Курс для подписки",
            description="desc",
            owner=self.user
        )

        self.subscription_url = reverse("course-subscription")
        self.course_detail_url = reverse("course-detail", args=[self.course.id])
        self.course_list_url = reverse("course-list")

    def test_toggle_subscription_add_and_remove(self):
        self.client.force_authenticate(user=self.user)

        resp1 = self.client.post(self.subscription_url, data={"course_id": self.course.id}, format="json")
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assertEqual(resp1.data["is_subscribed"], True)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        resp2 = self.client.post(self.subscription_url, data={"course_id": self.course.id}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data["is_subscribed"], False)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_subscribed_in_course_response(self):
        self.client.force_authenticate(user=self.user)

        resp0 = self.client.get(self.course_detail_url)
        self.assertEqual(resp0.status_code, status.HTTP_200_OK)
        self.assertEqual(resp0.data["is_subscribed"], False)

        self.client.post(self.subscription_url, data={"course_id": self.course.id}, format="json")

        resp1 = self.client.get(self.course_detail_url)
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assertEqual(resp1.data["is_subscribed"], True)

    def test_courses_list_has_pagination_structure(self):
        self.client.force_authenticate(user=self.user)

        resp = self.client.get(self.course_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("count", resp.data)
        self.assertIn("results", resp.data)
