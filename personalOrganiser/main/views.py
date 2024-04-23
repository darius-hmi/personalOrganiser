from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm, FoodForm, datePicker, ExerciseForm, toDoForm, MessageForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, Food, Exercise, toDoList, Message, Thread
from datetime import datetime, time
from django.db.models import Sum
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import Http404

@login_required(login_url='/login')
def home(request):
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            # Check if the logged-in user is the author or has permission to delete the post
            if request.user == post.author:
                post.delete()
    posts = Post.objects.all()
    return render(request, 'main/home.html', {"posts": posts}) 



@login_required(login_url='/login')
def todaysFood(request):
    author = request.user
    todaysFoods = Food.objects.filter(author=author, created_at__date=datetime.today().date())
    totalCalories = todaysFoods.aggregate(Sum('calories'))['calories__sum']
    totalProtein = todaysFoods.aggregate(Sum('protein'))['protein__sum']


    if request.method == 'POST':
        food_id = request.POST.get('food-id')
        food = Food.objects.filter(id=food_id).first()
        food.delete()
        todaysFoods = Food.objects.filter(author=author, created_at__date=datetime.today().date())
        totalCalories = todaysFoods.aggregate(Sum('calories'))['calories__sum']
        totalProtein = todaysFoods.aggregate(Sum('protein'))['protein__sum']


    return render(request, 'main/todaysFood.html', {'todaysFoods':todaysFoods, 'totalCalories':totalCalories, 'totalProtein':totalProtein}) 



@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form':form})

@login_required(login_url='/login')
def create_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.author = request.user
            food.save()
            return redirect('/home')
    else:
        form = FoodForm()
    
    return render(request, 'main/create_food.html', {'form':form})


@login_required(login_url='/login')
def foodDiary(request):
    if request.method == 'POST':
        form = datePicker(request.POST)
        if form.is_valid():
            # Handle datePicker form submission
            d = form.cleaned_data['date']
            author = request.user
            todaysFoods = Food.objects.filter(author=author, created_at__date=d)
            totalCalories = todaysFoods.aggregate(Sum('calories'))['calories__sum']
            totalProtein = todaysFoods.aggregate(Sum('protein'))['protein__sum']

            return render(request, 'main/foodDiary.html', {'form': form, 'todaysFoods': todaysFoods, 'totalCalories': totalCalories, 'totalProtein': totalProtein})

        # Handle delete action
        form_type = request.POST.get('form-type')
        if form_type == 'delete-form':
            food_id_to_delete = request.POST.get('food-id')
            if food_id_to_delete:
                food_to_delete = Food.objects.filter(id=food_id_to_delete).first()
                food = get_object_or_404(Food, id=food_id_to_delete)
                d = food.created_at.date()
                author = request.user
                todaysFoods = Food.objects.filter(author=author, created_at__date=d)
                totalCalories = todaysFoods.aggregate(Sum('calories'))['calories__sum']
                totalProtein = todaysFoods.aggregate(Sum('protein'))['protein__sum']
                if food_to_delete:
                    food_to_delete.delete()
                    todaysFoods = Food.objects.filter(author=author, created_at__date=d)
                    totalCalories = todaysFoods.aggregate(Sum('calories'))['calories__sum']
                    totalProtein = todaysFoods.aggregate(Sum('protein'))['protein__sum']
                    # Redirect to refresh the page without the deleted entry
                    return render(request, 'main/foodDiary.html', {'form': form, 'todaysFoods': todaysFoods, 'totalCalories': totalCalories, 'totalProtein': totalProtein})

    else:
        form = datePicker()

    return render(request, 'main/foodDiary.html', {'form': form})



@login_required(login_url='/login')
def exerciseDiary(request):
    if request.method == 'POST':
        form = datePicker(request.POST)
        if form.is_valid():
            # Handle datePicker form submission
            d = form.cleaned_data['date']
            author = request.user
            todaysExercises = Exercise.objects.filter(author=author, created_at__date=d)
            return render(request, 'main/exerciseDiary.html', {'form':form, 'todaysExercises':todaysExercises})

        # Handle delete action
        form_type = request.POST.get('form-type')
        if form_type == 'delete-form':
            exercise_id_to_delete = request.POST.get('exercise-id')
            if exercise_id_to_delete:
                exercise_to_delete = Exercise.objects.filter(id=exercise_id_to_delete).first()
                exercise = get_object_or_404(Exercise, id=exercise_id_to_delete)
                d = exercise.created_at.date()
                author = request.user
                todaysExercises = Exercise.objects.filter(author=author, created_at__date=d)
                if exercise_to_delete:
                    exercise_to_delete.delete()
                    todaysExercises = Exercise.objects.filter(author=author, created_at__date=d)
                    # Redirect to refresh the page without the deleted entry
                    return render(request, 'main/exerciseDiary.html', {'form':form, 'todaysExercises':todaysExercises})
    else:
        form = datePicker()

    return render(request, 'main/exerciseDiary.html', {'form': form})

@login_required(login_url='/login')
def add_Exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.author = request.user
            exercise.save()
            return redirect('/home')
    else:
        form = ExerciseForm()
    
    return render(request, 'main/add_exercise.html', {'form':form})

@login_required(login_url='/login')
def add_toDoList(request):
    if request.method == 'POST':
        form = toDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            return redirect('/home')
    else:
        form = toDoForm()
    
    return render(request, 'main/add_toDoList.html', {'form':form})

@login_required(login_url='/login')
def viewToDoList(request):
    author = request.user
    toDoItems = toDoList.objects.filter(author=author)
    # Tested the below def so it sends an email reminder to the 
    #send_mail_test(author)
    form_type = request.POST.get('form-type')
    if form_type == 'delete-form':
        todo_id_to_delete = request.POST.get('todo-id')
        if todo_id_to_delete:
            todo_to_delete = toDoList.objects.filter(id=todo_id_to_delete).first()
            author = request.user
            toDoItems = toDoList.objects.filter(author=author)
            if todo_to_delete:
                todo_to_delete.delete()
                toDoItems = toDoList.objects.filter(author=author)
                # Redirect to refresh the page without the deleted entry
                return render(request, 'main/toDoList.html', {'toDoItems':toDoItems})


    return render(request, 'main/toDoList.html', {'toDoItems':toDoItems})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/sign_up.html', {"form":form})


@login_required(login_url='/login')
def add_food(request, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    form = FoodForm(request.POST)
    if form.is_valid():
        food = form.save(commit=False)
        food.author = request.user
        food.created_at = datetime.combine(date_obj, datetime.min.time())
        food.save()
        return redirect('foodDiary')
    else:
        form = FoodForm()

    return render(request, 'main/add_food_with_date.html', {'form': form, 'date': date})

@login_required(login_url='/login')
def add_exerciseToDate(request, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    form = ExerciseForm(request.POST)
    if form.is_valid():
        exercise = form.save(commit=False)
        exercise.author = request.user
        exercise.created_at = datetime.combine(date_obj, datetime.min.time())
        exercise.save()
        return redirect('exerciseDiary')
    else:
        form = ExerciseForm()

    return render(request, 'main/add_exercise_with_date.html', {'form': form, 'date': date})


#The below definition is sending an email to the yahoo account when used. Need to use Celery to send automatically
# def send_mail_test(author):
#     tomorrow = timezone.now() + timezone.timedelta(days=1)
#     tasks_due_tomorrow = toDoList.objects.filter(dueDate__range=(tomorrow, tomorrow + timezone.timedelta(days=1)), author=author)

#     for task in tasks_due_tomorrow:
#         subject =  'Test Email'
#         message = task.task + " is due tomorrow!"
#         from_email = ''
#         recipient_list = ['']

#         send_mail(subject, message, from_email, recipient_list)


@login_required
def initiate_dm(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, pk=recipient_id)

        # Check if a thread between the current user and recipient already exists
        thread = Thread.objects.filter(participants=request.user).filter(participants=recipient).first()
        if thread is None:
            # If thread doesn't exist, create a new one
            thread = Thread.objects.create()
            thread.participants.add(request.user, recipient)

        return redirect('thread_detail', thread_id=thread.id)
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'main/initiate_dm.html', {'users': users})



@login_required
def thread_list_view(request):
    threads = Thread.objects.filter(participants=request.user)
    return render(request, 'main/thread_list.html', {'threads': threads})

@login_required
def thread_detail_view(request, thread_id):
    try:
        thread = Thread.objects.get(pk=thread_id, participants=request.user)
    except Thread.DoesNotExist:
        raise Http404("Thread does not exist")

    messages = thread.messages.all()
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.thread = thread
            message.save()
            return redirect('thread_detail', thread_id=thread.id)
    return render(request, 'main/thread_detail.html', {'thread': thread, 'messages': messages, 'form': form})
