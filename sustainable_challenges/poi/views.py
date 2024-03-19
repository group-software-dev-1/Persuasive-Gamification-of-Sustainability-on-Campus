from typing import Any
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseForbidden
from .models import PlaceOfInterest, VisitedPlaceOfInterest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .forms import PlaceOfInterestForm, LocationForm
from json import dumps
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def submit(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponseForbidden:
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
    if not request.user.is_staff:
        return HttpResponseForbidden()

    submitted = False
    id = -1
    if request.method == "POST":
        # Populate the form with the POST data
        form = PlaceOfInterestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            poi = PlaceOfInterest.objects.get(pk=obj.id)
            return HttpResponseRedirect(f'/poi/submit?submitted=True&id={poi.id}')
    else:  # Is a GET request
        # Create a blank form
        form = PlaceOfInterestForm
        # Check if the GET request is a result of the redirect after a post
        if 'submitted' in request.GET and 'id' in request.GET:
            submitted = True
            id = request.GET['id']

    return render(request, 'poi/submit.html', {'form': form, 
                                                'submitted': submitted, 
                                                'id': id,
                                                'is_staff': request.user.is_staff})

def information(request, poi_id):
    poi = get_object_or_404(PlaceOfInterest, pk=poi_id)
    submitted = False
    close = False
    visited = False

    try:
        VisitedPlaceOfInterest.objects.get(user=request.user, place=poi)
        visited = True
    except ObjectDoesNotExist:
        visited = False

    if request.method == "POST" and visited == False:
        form = LocationForm(request.POST)
        if form.is_valid():
            lat = float(form.cleaned_data['lat'])
            lon = float(form.cleaned_data['lon'])
            lat_delta = abs(lat - float(poi.lat)) 
            lon_delta = abs(lon - float(poi.lon)) 
            if lat_delta <= 0.001 and lon_delta <= 0.001:  # 111 meter difference
                close = True
                VisitedPlaceOfInterest.objects.create(user=request.user, place=poi)

            return HttpResponseRedirect(f'/poi/info/{poi_id}?submitted=True&close={close}')
    else:
        form = LocationForm
        if 'submitted' in request.GET and 'close' in request.GET:
            submitted = True
            close = request.GET['close']

    json_dict = {'lat': poi.lat, 'lon': poi.lon, 'close': close}

    return render(request, 'poi/info.html', {'visited': visited,
                                             'close': close,
                                             'submitted': submitted,
                                             'poi': poi,
                                             'lat_lon': json_dict,
                                             'form': form,
                                             'is_staff': request.user.is_staff})

def map(request):
    pois = PlaceOfInterest.objects.all()
    poi_list = []
    for poi in pois:
        poi_list.append({'title': poi.title, 'desc': poi.desc, 'lat': poi.lat, 'lon': poi.lon, 'id': poi.id})
    json_dict = {'places': poi_list}
    return render(request, 'poi/map.html', {'json_dict': json_dict,
                                            'is_staff': request.user.is_staff})

