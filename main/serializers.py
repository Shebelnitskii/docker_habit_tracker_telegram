from rest_framework import serializers

from .models import Habit, TimeAndPlace


class TimeAndPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeAndPlace
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    time_place = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = '__all__'

    def get_time_place(self, obj):
        # Получаем связанные объекты TimeAndPlace для данной привычки
        time_places = obj.time_place.all()
        return TimeAndPlaceSerializer(time_places, many=True).data
