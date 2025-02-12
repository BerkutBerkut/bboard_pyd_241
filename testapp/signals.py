from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from testapp.models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        """
        Создание профиля для нового пользователя
        """
        Profile.objects.create(user=instance)
    else:
        """
        Добавление недостающих профилей для существующих пользователей.
        """
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Отправляет приветственное письмо новому пользователю
    """
    if created:
        send_mail(
            "Добро пожаловать!",
            f"Привет, {instance.username}! Спасибо за регистрацию.",
            "admin@mysite.com",
            [instance.email],
            fail_silently=True,
        )
