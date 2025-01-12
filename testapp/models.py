from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)
    notes = GenericRelation("Note", related_query_name='spare')


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit',
                                    through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', 
                                       fk_field='object_id')


# 1. Прямое наследование
class Message(models.Model):
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f"Message: {self.content[:20]}"


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE,
                                   parent_link=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f"PrivateMessage to {self.user.username}"

# Двойное последовательное наследование
class MegaPrivateMessage(PrivateMessage):
    priority = models.IntegerField(default=1)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    class Meta:
        ordering = ['-priority',  '-published']

    def __str__(self):
        return f"MegaPrivateMessage to {self.user.username}, Priority: {self.priority}"
    


# 2. Абстрактные модели
# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()

#     class Meta:
#         abstract = True
#         # ordering = ["name"]

# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None

#     # class Met:
#     #     ordering = ['order', 'name']


class SMS(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
    