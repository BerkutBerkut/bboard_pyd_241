from django.db import models
from django.contrib.auth.models import User


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)




class SMS(models.Model):
   
    KINDS = (
        (None),
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default="s",
    )

    rubric = models.ForeignKey(
        "Rubric",
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Рубрика",
        
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Сообщение",
        
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Текст сообщения",
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    class Meta:
        ordering = ["-published", "title"]
        # order_with_respect_to = 'rubric'

 