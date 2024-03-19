from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from study_area.models import Event
import requests


#function that gets the router ip 
def get_router_ip(request):
    #uses this api i found to just return the routers public ip
    response = requests.get('https://api.ipify.org?format=json')
    router_ip = response.json()['ip']
    return router_ip

class RouterAccessMiddleware:

    #initializes the middleware
    def __init__(self, get_response):
        self.get_response = get_response
    #invokes the middleware for all incoming requests
    def __call__(self, request):
        response = self.get_response(request)
        #if the path of the request is of the event_details (the page where you attend the event)
        if request.path.startswith('/study_area/event_details/'):
            #then gets the id from the url
            event_id = request.path.split('/')[-2]
            #gets the event object with the corresponding ip
            try:
                event = Event.objects.get(pk=event_id)
            except Event.DoesNotExist:
                return render(request, 'study_area/invalid_event.html')
            #gets the users ip
            user_ip = get_router_ip(request)
            #checks if the user is an admin
            is_admin = request.user.is_authenticated and request.user.is_staff
            #if the user isnt an admin and the ips dont match
            if user_ip != event.router_ip and not is_admin:
                #they arent allowed access and are sent to invalid page
                return HttpResponseRedirect(reverse('restricted_access'))
        #otherwise lets it happen
        return response
