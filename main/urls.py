from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    #path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('create-food', views.create_food, name='create_food'),
    path('todaysFood', views.todaysFood, name='todaysFood'),
    path('foodDiary', views.foodDiary, name='foodDiary'),
    path('addExercise', views.add_Exercise, name='add_Exercise'),
    path('exerciseDiary', views.exerciseDiary, name='exerciseDiary'),
    path('addToDoList', views.add_toDoList, name='add_toDo'),
    path('toDoList', views.viewToDoList, name='toDoList'),
    path('foodDiary/add/<str:date>/', views.add_food, name='add_food_with_date'),
    path('exerciseDiary/add/<str:date>/', views.add_exerciseToDate, name='add_exercise_with_date'),
    path('threads/', views.thread_list_view, name='thread_list'),
    path('thread/<int:thread_id>/', views.thread_detail_view, name='thread_detail'),
    path('dm/<int:recipient_id>/', views.initiate_dm, name='initiate_dm'),
    path('initiate-dm/', views.initiate_dm, name='initiate_dm'),
    path('get_exercise_data/', views.get_exercise_data, name='get_exercise_data'),
    path('profile/', views.profile_view, name='profile'),
]