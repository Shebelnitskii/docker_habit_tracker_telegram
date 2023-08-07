from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        linked_habit = data.get('linked_habit')
        reward = data.get('reward')
        good_habit_sign = data.get('good_habit_sign')
        if linked_habit and reward:
            raise serializers.ValidationError('Связанная привычка и вознаграждение не могут быть указаны одновременно')
        elif good_habit_sign and (reward is not None or linked_habit is not None):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки!")
        return data