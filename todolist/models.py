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