from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from teach.models import Solved

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Konto zostało utworzone!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        
        
        logout(request)
        return render(request, 'users/logout.html')
    return redirect(request, 'teach-home')

class UserLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        solved_objects = user.solved_set.all()
        self.request.session['solved_exercises'] = {solved.exercise.id : solved.correct  for solved in solved_objects}
        self.request.session.modified = True

        return response