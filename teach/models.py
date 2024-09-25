from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now


class Category(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.name}'


class Exercise(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField()
    image = models.ImageField(default=None, blank=True, null=True, upload_to='images')
    solution = models.TextField(default="", blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    class_profile = models.CharField(default='podstawa', max_length=64)
    
    def __str__(self):
        return f'{self.category}. {self.description[:50]}'
    

class Answer(models.Model):
    text = models.TextField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.text}.{self.correct} for {self.exercise}'

    
class Solved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    
class Teaches(models.Model):
    teacher = models.ForeignKey(User, related_name='students', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='teachers', on_delete=models.CASCADE)
    start = models.DateTimeField(db_default=Now())

    
class Struggles(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)