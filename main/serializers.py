from rest_framework import serializers

from main.models import Habit, TimeAndPlace


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class TimeAndPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeAndPlace
        fields = '__all__'
