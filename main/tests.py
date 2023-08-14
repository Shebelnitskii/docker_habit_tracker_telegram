from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Habit
from .serializers import HabitSerializer
from datetime import time


# Create your tests here.


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test", password="testpassword", chat_id=123456789
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тестирование создание привычки"""
        data = {
            "action": "test habit",
            "good_habit_sign": "True",
            "is_public": "False",
            "time": "09:00:00",
            "periodicity": 2,
            "time_to_complete": 120,
            "place": "test",
        }

        response = self.client.post("/habit/create/", data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(
            response.json(),
            {
                "id": 3,
                "action": "test habit",
                "place": "test",
                "time": "09:00:00",
                "time_to_complete": 120,
                "periodicity": 2,
                "good_habit_sign": True,
                "reward": None,
                "is_public": False,
                "linked_habit": None,
                "owner": self.user.id,
            },
        )

        self.assertTrue(Habit.objects.all().exists())

    def test_list_habit(self):
        """Тестирование просмотра списка привычек"""

        habit = Habit.objects.create(
            action="test habit list",
            good_habit_sign="True",
            is_public="False",
            time="09:00:00",
            periodicity=2,
            time_to_complete=120,
            place="test list",
            owner=self.user,
        )

        response = self.client.get(
            "/habit/",
        )

        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": habit.id,
                    "action": "test habit list",
                    "place": "test list",
                    "time": "09:00:00",
                    "time_to_complete": 120,
                    "periodicity": 2,
                    "good_habit_sign": True,
                    "reward": None,
                    "is_public": False,
                    "linked_habit": None,
                    "owner": self.user.id,  # Используем первичный ключ пользователя
                }
            ],
        }

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), expected_data)

    def test_detail_habit(self):
        """Тестирование просмотра деталей привычки"""
        habit = Habit.objects.create(
            action="test habit detail",
            good_habit_sign="True",
            is_public="False",
            time="09:00:00",
            periodicity=2,
            time_to_complete=120,
            place="test detail",
            owner=self.user,
        )

        url = f"/habit/detail/{habit.pk}/"

        response = self.client.get(url)

        expected_data = {
            "id": habit.id,  # Используем первичный ключ урока
            "action": "test habit detail",
            "place": "test detail",
            "time": "09:00:00",
            "time_to_complete": 120,
            "periodicity": 2,
            "good_habit_sign": True,
            "reward": None,
            "is_public": False,
            "linked_habit": None,
            "owner": self.user.id,  # Используем первичный ключ пользователя
        }

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), expected_data)

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        # Создаем тестовый курс и урок
        habit = Habit.objects.create(
            action="test habit delete",
            good_habit_sign="True",
            is_public="False",
            time="09:00:00",
            periodicity=2,
            time_to_complete=120,
            place="test delete",
            owner=self.user,
        )

        url = f"/habit/delete/{habit.pk}/"

        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что урок был удален из базы данных
        self.assertFalse(Habit.objects.filter(pk=habit.pk).exists())

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        habit = Habit.objects.create(
            action="test habit update",
            good_habit_sign="True",
            is_public="False",
            time="09:00:00",
            periodicity=2,
            time_to_complete=120,
            place="test update",
            owner=self.user,
        )

        url = f"/habit/update/{habit.pk}/"

        data = {
            "action": "updated habit",
            "good_habit_sign": "False",
            "is_public": "True",
            "time": "10:00:00",
            "periodicity": 3,
            "time_to_complete": 180,
            "place": "updated place",
        }

        response = self.client.put(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Обновляем ожидаемые данные для сравнения
        expected_data = {
            "id": habit.id,
            "action": "updated habit",
            "place": "updated place",
            "time": "10:00:00",
            "time_to_complete": 180,
            "periodicity": 3,
            "good_habit_sign": False,
            "reward": None,
            "is_public": True,
            "linked_habit": None,
            "owner": self.user.id,
        }

        # Проверяем, что данные после обновления соответствуют ожидаемым данным
        self.assertEquals(response.json(), expected_data)

        # Проверяем, что привычка была действительно обновлена в базе данных
        updated_habit = Habit.objects.get(pk=habit.pk)
        self.assertEquals(updated_habit.action, "updated habit")
        self.assertEquals(updated_habit.place, "updated place")
        self.assertEquals(updated_habit.time.strftime("%H:%M:%S"), "10:00:00")
        self.assertEquals(updated_habit.time_to_complete, 180)
        self.assertEquals(updated_habit.periodicity, 3)
        self.assertFalse(updated_habit.good_habit_sign)
        self.assertTrue(updated_habit.is_public)


class UserTestCase(APITestCase):
    def test_create_user(self):
        """Тестирование создания пользователя"""
        user = User.objects.create_user(
            username="test",
            password="testpassword",
            chat_id=123456789
        )
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Тестирование создания админа"""
        user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            chat_id=987654321
        )
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_create_api(self):
        """Тестирование создания пользователя через API"""

        data = {
            "username": "testuser",
            "password": "testpassword",
            "chat_id": 123456789
        }
        response = self.client.post("/users/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("testpassword"))


class HabitSerializerTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpassword",
        )

    def test_valid_habit_data(self):
        data = {
            "action": "test habit",
            "place": "home",
            "time": "09:00:00",
            "time_to_complete": 120,
            "periodicity": 7,
            "good_habit_sign": True,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        habit = serializer.save(owner=self.user)
        self.assertEqual(habit.action, "test habit")
        self.assertEqual(habit.place, "home")
        self.assertEqual(habit.time, time(9, 0))
        self.assertEqual(habit.time_to_complete, 120)
        self.assertEqual(habit.periodicity, 7)
        self.assertTrue(habit.good_habit_sign)
        self.assertFalse(habit.is_public)
        self.assertIsNone(habit.linked_habit)
        self.assertIsNone(habit.reward)
        self.assertEqual(habit.owner, self.user)

    def test_linked_habit_validation(self):
        parent_habit = Habit.objects.create(
            action="parent habit",
            place="home",
            time="09:00:00",
            time_to_complete=120,
            periodicity=7,
            good_habit_sign=True,
            is_public=False,
            owner=self.user
        )

        data = {
            "action": "child habit",
            "place": "office",
            "time": "15:00:00",
            "time_to_complete": 60,
            "periodicity": 3,
            "good_habit_sign": True,
            "is_public": False,
            "linked_habit": parent_habit.id,
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn("У приятной привычки не может быть вознаграждения или связанной привычки!",
                      serializer.errors["non_field_errors"][0])

    def test_good_habit_sign_with_reward_validation(self):
        data = {
            "action": "rewarded habit",
            "place": "home",
            "time": "09:00:00",
            "time_to_complete": 120,
            "periodicity": 7,
            "good_habit_sign": True,
            "is_public": False,
            "reward": "get a treat",
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn("У приятной привычки не может быть вознаграждения или связанной привычки!",
                      serializer.errors["non_field_errors"][0])
