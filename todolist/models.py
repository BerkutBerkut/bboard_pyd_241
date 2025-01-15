from django.db import models
from django.utils.timezone import now

class Todo(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Задача',
    )
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False) # Статус выполнения
    created_at = models.DateTimeField(auto_now_add=True) # Дата создания
    updated_at = models.DateTimeField(auto_now=True) # Дата обновления


    def __str__(self):
        return self.title 
