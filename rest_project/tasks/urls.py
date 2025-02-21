from django.urls import path
from tasks.views import (
    task,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    UserListView,
)

urlpatterns = [
    path('task/', task),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('users/', UserListView.as_view(), name='user-list',)
]
