from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Food(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    protein = models.IntegerField()
    calories = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '\n' + self.description

class Exercise(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    class muscleGroup(models.TextChoices):
        Chest = 'Chest', 'Chest'
        Shoulder = 'Shoulder', 'Shoulder'
        Back = 'Back', 'Back'
        Legs = 'Leg', 'Leg'
        Arms = 'Arms', 'Arms'
    muscle = models.CharField(
        max_length=10,
        choices = muscleGroup.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class toDoList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dueDate = models.DateField()
    task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task

class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)