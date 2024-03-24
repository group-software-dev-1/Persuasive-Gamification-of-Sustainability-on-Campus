from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from sustainable_challenges.middleware import get_router_ip
from authuser.models import User
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    is_staff = request.user.is_authenticated and request.user.is_staff
    return render(request, 'study_area/home.html', {"is_staff": is_staff})



@login_required
def event(request):
    #uses function to get the ip of the request sent
    router_ip = get_router_ip(request)
    #sets current time as current_time
    current_time = timezone.now()
    
    #Gets all of the events where the event start time is greater than the current time
    upcoming_events = Event.objects.filter(date_time__gte=current_time).order_by('date_time')
    
    #filters events that have passed but are within the duration
    current_events = []
    for event in Event.objects.all():
        #for all of the events, checks to see if the start time plus duration is less than the current time
        end_time = event.date_time + event.duration
        if current_time >= event.date_time and current_time <= end_time:
            #if it is attaches the newly calculate event end time and adds it to the current events list
            event.end_time = end_time  # Attach end time to the event object
            current_events.append(event)
    
    #basic context including if the user is staff
    is_staff = request.user.is_authenticated and request.user.is_staff
    context = {
        'router_ip': router_ip,
        'upcoming_events': upcoming_events,
        'current_events': current_events,
        'current_time': current_time,
        'is_staff': is_staff
    }
    return render(request, 'study_area/event.html', context)


#creation of evenets
@login_required
def create_event(request):
    #takes a post reqeuest and makes a new event using the event form
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.router_ip = get_router_ip(request)  # uses get_router_ip function from middleware to assign the ip of the event location to the event
            event.save()
            return redirect('home')  #redirects back to home when done
    else:
        form = EventForm()
    is_staff = request.user.is_authenticated and request.user.is_staff
    return render(request, 'study_area/create_event.html', {'form': form, 'is_staff': is_staff})


@login_required
def event_detail(request, event_id):
    #first checks if url is valid
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        #if no evenet for inputted url redirects to invalid_event
        return render(request, 'study_area/invalid_event.html')
    #creates a list of all the event attendess
    attendees = [] 
    if event.attendees:
        #then as attendess are stored as a comma sepereated string, splits it up and appends to the lsit
        attendees = event.attendees.split(',')
    
    #If a post reqeuest is recieved
    if request.method == 'POST':
        #gets the code attached and the username
        code = request.POST.get('code')
        username = request.user.username 
        #If the code is renew and the username is related to a staff
        if code == 'renew' and request.user.is_authenticated and request.user.is_staff:

            event.router_ip = get_router_ip(request) #Then re assigns the new ip to the event ip (incase of a ip renewal at event)
            event.save()

        elif code == 'attend':
            #If the code is attend and the username is not in attendess list
            if username not in attendees:
                #add the new username to the attendees string and saves it
                attendees.append(username)
                event.attendees = ','.join(attendees) 
                event.save()
                
                #then gets the user object with matching username and awards them the points associated with the event
                user = User.objects.get(username=username)
                user.complete_task('saving')
                user.save()
        
        #after redirects them back to the same event page
        return redirect('event_detail', event_id=event_id)
    
    #now for the html part
    #creates the end time of the event
    end_time = event.date_time + event.duration
    
    #if the event start time is in the future
    if event.date_time > timezone.now():
        event_state = 0  #event state is set as 0, or not started
    #if the end time is in the future
    elif end_time > timezone.now() > event.date_time:
        event_state = 1  #means it ongoing, sets as 1
    #otherwise it will be ended, if the user is an admin
    elif request.user.is_authenticated and request.user.is_staff:
        event_state = 2  #set as code 2
    else:
        #otherwise send them to invalid event page
        return redirect('invalid_event')  
    
    #basic context including if the user is staff
    is_staff = request.user.is_authenticated and request.user.is_staff
    context = {'event': event, 'is_staff': is_staff, 'event_state': event_state, 'user': request.user, 'attendees': attendees}
    return render(request, 'study_area/event_detail.html', context)





#simple views for basic pages
def invalid_event(request):
    return render(request, 'study_area/invalid_event.html')

def restricted_access(request):
    return render(request, 'study_area/restricted_access.html')