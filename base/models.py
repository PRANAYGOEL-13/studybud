from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



#at the start we used inbuilt user model but for the sake of more personalization we are creating our own user model
#from django.contrib.auth.models import User
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, null =True)
    email = models.EmailField(unique=True, null =True)
    bio = models.TextField(null=True, blank=True)#to make to field not compulsory we have to add "blank=True"


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

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
    
    