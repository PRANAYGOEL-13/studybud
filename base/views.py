# this file basically renders the urls and direct to there particular operation or path
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages #used for flash messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
#from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        user=authenticate(request, email=email,  password=password)    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or password does not exists') #doesn't goes away on refresh have to renter the url to make it go away
    context={'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    #page='register'
    form=MyUserCreationForm()

    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)#we are actually freezing the form so that we authenticate at our level
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context={'form':form}  #'page': page}
    return render(request, 'base/login_register.html', context)



    return render(request, 'base/login_register.html')

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else '' ## we are getting the query after the '?' to filter out that particular page
    
    # Q is used here so that we can add AND OR operations in the filter statement
    rooms =Room.objects.filter(Q(topic__name__icontains=q) | 
                               Q(name__icontains=q) | 
                               Q(description__icontains=q))  ## here we used topic__name to filter out that particular topic but then we added 
    
    room_count=rooms.count()
    topics=Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

    context={'rooms' : rooms, 'topics': topics,
             'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html',  context)

def room(request, pk): # pk here is the primary key we are getting from the url
    room=Room.objects.get(id=pk) #DJANGO CREATES THERE INCREMENTAL INTEGER ID FOR EVERY DIFFERENT OBJECTS IN 
                                 #THE MODEL SO WE CAN EASILY PASS pk TO id TO REACH THAT PARTICULAR ROOM
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if(request.method) == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
   
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user =User.objects.get(id=pk)
    rooms= user.room_set.all()
    room_messages =user.message_set.all()
    topics= Topic.objects.all()
    context={'user': user, 'rooms': rooms, 
             'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)





## THIS METHOD IS USED FOR CREATE OPERATION i.e CREATING ROOM 
@login_required(login_url='/login')
def createRoom(request):    
    form =RoomForm()
    topics=Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)  #now if we create a new topic then the value of created will be equal to true otherwise it will be false

        form=RoomForm(request.POST)


        #THIS IS ANOTHER WAY OF CREATING A ROOM AND THE ANOTHER ONE IS THE LATTER ONE form.save()
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        """if form.is_valid():
            room=form.save(commit=False)
            room.host = request.user
            form.save()"""
        return redirect('home')
        
    context={'form':form, 'topics':topics}
    return render( request, 'base/room_form.html', context)


## THIS METHOD IS USED FOR UPDATE OPERATION i.e CREATING ROOM 
@login_required(login_url='/login')
def updateRoom(request, pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room) ## now the instance is used to prefill the form making it easy for the user
    topics=Topic.objects.all()

    if request.user !=room.host: #restriction user to update other users account
        return HttpResponse('You are not allowed here!!!')

    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)  #now if we create a new topic then the value of created will be equal to true otherwise it will be false
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context={'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context )

# this is used for DELETION OPERATION 
## we are deleting rooms here which should not affect the topics as topic is the higher in hierarchy than
@login_required(login_url='/login')
def deleteRoom(request, pk):
    room =Room.objects.get(id=pk)

    if request.user !=room.host:#restriction user to delete other users account
        return HttpResponse('You are not allowed here!!!')


    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj' : room})



@login_required(login_url='/login')
def deleteMessage(request, pk):
    message =Message.objects.get(id=pk)

    if request.user != message.user:#restriction user to delete other users account
        return HttpResponse('You are not allowed here!!!')


    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj' : message})



def updateUser(request):
    user=request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)


    return render(request, 'base/update-user.html', {'form': form})




def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else '' ## we are getting the query after the '?' to filter out that particular page

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})