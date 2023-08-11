from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from main.permissions import IsPublicOrReadOnly, IsOwnerOrReadOnly
from main.models import Habit
from main.serializers import HabitSerializer
from main.pagination import HabitPagination
from main.tasks import send_habit_message

# Create your views here.


class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsPublicOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(Q(is_public=True) | Q(owner=user))
        else:
            return Habit.objects.filter(is_public=True)


class HabitCreateView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class HabitDetailView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class HabitDeleteView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
