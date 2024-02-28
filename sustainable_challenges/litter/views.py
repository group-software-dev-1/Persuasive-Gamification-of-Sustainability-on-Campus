from typing import Any
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import LitterInstance
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .forms import InstanceForm, ApproveForm, TimeRangeForm
from json import dumps

    
def latest(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for displaying a list (in date order) of instances that need approving/rejecting

    Parameters
    ----------
    request : HttpRequest
              The request object generated by django

    Returns
    -------
    HttpResponse
        Containing the latest.html webpage
    '''
    # Get the pending status instances and order them by oldest first
    valid_instances = LitterInstance.objects.filter(approved=0).order_by("-datetime")
    # Render the webpage
    return render(request, "litter/latest.html", {"latest_instance_list": valid_instances, 
                                                  "is_staff": request.user.is_staff})


def your_instances(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for displaying a list (in date order) of instances reported by the request user

    Parameters
    ----------
    request : HttpRequest
              The request object generated by django

    Returns
    -------
    HttpResponse
        Containing the your-instances.html webpage
    '''
    # Get the instances submitted by this user and order them by oldest first
    instance_list = LitterInstance.objects.filter(user_id=request.user.id).order_by("-datetime")
    # Render the webpage
    return render(request, "litter/your-instances.html", {"instance_list": instance_list, 'is_staff': request.user.is_staff})

    
def instance(request: HttpRequest, instance_id: int) -> HttpResponse | HttpResponseRedirect:
    '''
    Endpoint for displaying a single instance of litter.
    If a staff user accesses this page, the instance is pending and they're not the one who made the report,
    there will be an option to approve or reject the instance

    Parameters
    ----------
    request : HttpRequest
              The request object generated by django
    instance_id : int
                  The id for the litter instance to view

    Returns
    -------
    HttpResponse or HttpResponseRedirect
        Containing the instance.html webpage.
        If HttpResponseRedirect it means that a POST request was received and accepted
    '''
    submitted = False
    _instance = get_object_or_404(LitterInstance, pk=instance_id)

    if request.method == 'POST':
        form = ApproveForm(request.POST)
        if form.is_valid():
            _instance.approved = form.cleaned_data['options']
            _instance.save()
            return HttpResponseRedirect(f'/litter/instance/{_instance.id}?submitted=True')
    else:
        form = ApproveForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'litter/instance.html', {'form': form,
                                                   'instance': _instance,
                                                   'submitted': submitted,
                                                   'id': _instance.id,
                                                   "requester_id": request.user.id,
                                                   "is_staff": request.user.is_staff})


def report(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    '''
    Endpoint for users to report an instance of litter on campus

    Parameters
    ----------
    request : HttpRequest
              The request object generated by django

    Returns
    -------
    HttpResponse or HttpResponseRedirect
        Containing the report.html webpage.
        If HttpResponseRedirect it means that a POST request was received and some litter was reported
    '''
    submitted = False
    id = -1
    if request.method == "POST":
        # Populate the form with the POST and FILES data
        form = InstanceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.datetime = timezone.now()  # Add current time
            # lat and lon had to be done in a different part to the model form
            # because the javascript needs to change it
            obj.lat = float(request.POST['lat_field'])
            obj.lon = float(request.POST['lon_field'])
            obj.user_id = request.user.id
            obj.save()
            _instance = LitterInstance.objects.get(datetime=obj.datetime, user_id=obj.user_id)
            return HttpResponseRedirect(f'/litter/report?submitted=True&id={_instance.id}')
    else:  # Is a GET request
        # Create a blank form
        form = InstanceForm
        # Check if the GET request is a result of the redirect after a post
        if 'submitted' in request.GET and 'id' in request.GET:
            submitted = True
            id = request.GET['id']

    return render(request, 'litter/report.html', {'form': form, 
                                                  'submitted': submitted, 
                                                  'id': id,
                                                  'is_staff': request.user.is_staff})


def heatmap(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    '''
    Endpoint for staff to view the heatmap of litter on campus.
    There is a form that allows the user to change the datetime range of litter reports that will be
    displayed on the map

    Parameters
    ----------
    request : HttpRequest
              The request object generated by django

    Returns
    -------
    HttpResponse or HttpResponseRedirect
        Containing the heatmap.html webpage.
        If HttpResponseRedirect it means that a POST request was received for changing the datetime range to view
    '''
    data = []
    if request.method == 'POST':
        form = TimeRangeForm(request.POST)
        if form.is_valid():
            # Extract the date range
            start_date = form.cleaned_data['s_date'].date()
            end_date = form.cleaned_data['e_date'].date()
            return HttpResponseRedirect(f'/litter/heatmap?start_date={start_date}&end_date={end_date}')
    else:  # Is a GET request
        form = TimeRangeForm
        # If the GET request is a result of the redirect after a post then these GET variables will exist
        if 'start_date' in request.GET and 'end_date' in request.GET:
            # Get instances that are within the specified time range
            approved_instances = LitterInstance.objects.filter(approved=1, datetime__range=[request.GET['start_date'], request.GET['end_date']])
        else:  # If its a GET request without being the result of a redirect
            approved_instances = LitterInstance.objects.filter(approved=1)  # All approved posts
        
        # Convert the data into the form accepted for the heatmap
        for _instance in approved_instances:
            data.append([float(_instance.lat), float(_instance.lon), 1])
        
        # JSON encode it
        dataJSON = dumps(data)
    
        return render(request, 'litter/heatmap.html', {'data': dataJSON,
                                                       'form': form,
                                                   'is_staff': request.user.is_staff})
