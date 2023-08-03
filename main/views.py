from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from main.models import Habit, TimeAndPlace
from main.serializers import HabitSerializer, TimeAndPlaceSerializer


# Create your views here.

class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]


class HabitCreateView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitDetailView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitDeleteView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class TimeAndPlaceListView(generics.ListAPIView):
    queryset = TimeAndPlace.objects.all()
    serializer_class = TimeAndPlaceSerializer


class TimeAndPlaceCreateView(generics.CreateAPIView):
    queryset = TimeAndPlace.objects.all()
    serializer_class = TimeAndPlaceSerializer
