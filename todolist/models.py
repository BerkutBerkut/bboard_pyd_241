from django.db import models
from django.utils.timezone import now


class Todo(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Задача',
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание") # Описание
    completed = models.BooleanField(default=False, verbose_name="Выполнено") # Статус выполнения
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания") # Дата создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления") # Дата обновления

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]


class Img(models.Model):
    img = models.ImageField(verbose_name="Изображение", upload_to='images/', blank=True, null=True)
    desc = models.TextField(verbose_name="Описание", null=True)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"

class Doc(models.Model):
    file = models.FileField(verbose_name='Документ', upload_to='documents/', blank=True, null=True)
    desc = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документ"