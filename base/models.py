from django.db import models
from django.contrib.auth.models import AbstractUser



#at the start we used inbuilt user model but for the sake of more personalization we are creating our own user model
#from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null =True)
    email = models.EmailField(unique=True, null =True)
    bio = models.TextField(null=False)#to make to field not compulsory we have to add "blank=True"

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null and blank are true so that 
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)#changes every time we save an update
    created = models.DateTimeField(auto_now_add=True)#doesn't matter how many time we save

    class Meta:
        ordering = ['-updated', '-created']  ##['updated', 'created'] if we do it without dash then it will be in ascending order i.e.
                                             ##newest item will be last

    def __str__(self):
        return self.name
    

# user, room are one to many relation mode i,e message can only have one user but one user can have multiple message
class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) #User is the built in model provided by the django
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated = models.DateTimeField(auto_now=True)#changes every time we save an update
    created = models.DateTimeField(auto_now_add=True)#doesn't matter how many time we save

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] #so that we only see a part of the message and it doesn't clutter up the admin page
    
    