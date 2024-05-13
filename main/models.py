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
    class names(models.TextChoices):
        flatBenchPressBB = 'Flat barbell bench press', 'Flat barbell bench press',
        inclineBenchPressBB = 'Incline barbell bench press', 'Incline barbell bench press',
        flatBenchPressDB = 'flat dumbbell Bench Press','flat dumbbell Bench Press',
        inclineBenchLowAngleDB = 'Incline dumbbell press low angle','Incline dumbbell press low angle',
        inclineBenchhighAngleDB = 'Incline dumbbell press high angle','Incline dumbbell press high angle',
        flyesDB = 'Dumbbell flyes', 'Dumbbell flyes',
        FlyesCable = 'Cable flyes', 'Cable flyes',
        machineFlyes = 'Machine flyes','Machine flyes',
        machineChestPress = 'Machine Chest Press','Machine Chest Press',

        shoulderPressDB = 'Dumbbell shoulder press', 'Dumbbell shoulder press',
        shoulderPressBB = 'Barbell Dumbbell press','Barbell Dumbbell press',
        lateralRaisesCable = 'Cable lateral raises','Cable lateral raises',
        lateralRaisesDB = 'Dumbbell lateral raises','Dumbbell lateral raises',
        frontRaisesDB = 'Dumbbell Front Raises','Dumbbell Front Raises',
        frontRaisesCable = 'Cable Front Raises','Cable Front Raises',
        frontRaises = 'Front Raises','Front Raises',
        rearDeltMachine = 'Rear Delt Machine','Rear Delt Machine',
        rearDeltDB = 'Rear Delt Dumbbell','Rear Delt Dumbbell',
        machineShoulderPress = 'Machine shoulder press','Machine shoulder press',
    
        bentOverRowBB = 'Barbell Bent over row','Barbell Bent over row',
        ropePulldown = 'Rope Pulldown','Rope Pulldown',
        deadlift = 'Deadlift', 'Deadlift',
        latPulldownStraightBar = 'Lat pulldown straight bar','Lat pulldown straight bar',
        latPulldownCloseGrip = 'Lat pulldown close grip','Lat pulldown close grip',
        cableRowWide = 'Cable row wide', 'Cable row wide', 
        cableRowNarrow = 'Cable row narrow', 'Cable row narrow',
        singleArmLatPulldown = 'Single arm lat pulldown','Single arm lat pulldown',
        machineRow = 'Machine Row', 'Machine Row',
        pullUps = 'pull ups','pull ups',
    
        squats = 'Squats','Squats',
        legPress = 'Leg press', 'Leg press',
        LegExtension = 'Leg extension', 'Leg extension',
        LegCurls = 'Leg curls','Leg curls',
        bulgarianSquats = 'Bulgarian split squats','Bulgarian split squats',
        rdl = 'Romian deadlift','Romian deadlift',

        bicepCurls = 'Bicep curls','Bicep curls',
        hammerCurls = 'Hamemr curls','Hamemr curls',
        bicepCurlCable = 'Cable bicep curls', 'Cable bicep curls', 
        hammerCurlsCable = 'Cable hammer curl','Cable hammer curl',

        tricepExtentionCable = 'Cable tricep extension','Cable tricep extension',
        tricepExtensionBar = 'Bar tricep extension','Bar tricep extension',
        overheadExtnsion = 'Overhead extension','Overhead extension',
        dips = 'Dips','Dips',



    name = models.CharField(
        max_length=50,
        choices = names.choices
    )

    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    class muscleGroup(models.TextChoices):
        Chest = 'Chest', 'Chest'
        Shoulder = 'Shoulder', 'Shoulder'
        Back = 'Back', 'Back'
        Legs = 'Legs', 'Legs'
        Arms = 'Arms', 'Arms'
    muscle = models.CharField(
        max_length=10,
        choices = muscleGroup.choices
    )
    created_at = models.DateTimeField(default=timezone.now)
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