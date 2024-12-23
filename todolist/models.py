from django.db import models

# class Todo(models.Model):
#     title = models.CharField(
#         max_length=50,
#         verbose_name='Задача',
#     )


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    items_list = models.JSONField(default=list)  # Поле для списка

    def __str__(self):
        return self.title
