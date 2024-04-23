from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Food, Exercise, toDoList, Message

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories', 'protein']

class toDoForm(forms.ModelForm):
    class Meta:
        model = toDoList
        fields = ['task', 'dueDate']
        labels = {'dueDate': 'Due Date'}
        widgets = {'dueDate':forms.DateInput(
            attrs={'type': 'date'}
        )}

class DateInput(forms.DateInput):
    input_type = 'date'

class datePicker(forms.Form):
    date = forms.DateField(widget=DateInput)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle', 'weight', 'sets', 'reps']
    

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    