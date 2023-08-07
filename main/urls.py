from django.urls import path
from main.apps import MainConfig
from main.views import HabitListView, HabitDeleteView, HabitDetailView, HabitUpdateView, HabitCreateView

app_name = MainConfig.name

urlpatterns = [
    path('habit/', HabitListView.as_view(), name='habit-list'),
    path('habit/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habit/detail/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habit/delete/<int:pk>/', HabitDeleteView.as_view(), name='habit-delete'),
    path('habit/update/<int:pk>/', HabitUpdateView.as_view(), name='habit-update'),
]
