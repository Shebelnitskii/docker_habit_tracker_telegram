from django.shortcuts import render
from rest_framework import generics

from main.serializers import HabitSerializer


# Create your views here.

class HabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()

class HabitCreateView(generics.CreateAPIView):
    serializer_class = HabitSerializer