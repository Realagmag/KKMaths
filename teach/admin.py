from django.contrib import admin
from .models import Exercise, Answer, Category, Solved, Struggles, Teaches

# Register your models here.
admin.site.register(Exercise)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Solved)
admin.site.register(Struggles)
admin.site.register(Teaches)