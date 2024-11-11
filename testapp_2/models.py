from django.db import models


class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name="Новая рубрика",
    )

   