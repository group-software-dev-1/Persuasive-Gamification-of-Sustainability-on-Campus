from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import LitterInstance
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import InstanceForm, ApproveForm, TimeRangeForm
from json import dumps

    
def latest(request):
    valid_instances = LitterInstance.objects.filter(approved=0).order_by("-datetime")
    return render(request, "litter/latest.html", {"latest_instance_list": valid_instances, 
                                                  "is_staff": request.user.is_staff})


def your_instances(request):
    instance_list = LitterInstance.objects.filter(user_id=request.user.id).order_by("-datetime")
    return render(request, "litter/your-instances.html", {"instance_list": instance_list})

    
def instance(request, instance_id):
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


def report(request):
    submitted = False
    id = -1
    if request.method == "POST":
        form = InstanceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.datetime = timezone.now()
            obj.lat = float(request.POST['lat_field'])
            obj.lon = float(request.POST['lon_field'])
            obj.user_id = request.user.id
            obj.save()
            _instance = LitterInstance.objects.get(datetime=obj.datetime, user_id=obj.user_id)
            return HttpResponseRedirect(f'/litter/report?submitted=True&id={_instance.id}')
    else:
        form = InstanceForm
        if 'submitted' in request.GET and 'id' in request.GET:
            submitted = True
            id = request.GET['id']

    return render(request, 'litter/report.html', {'form': form, 
                                                  'submitted': submitted, 
                                                  'id': id})


def heatmap(request):
    data = []
    if request.method == 'POST':
        form = TimeRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['s_date'].date()
            end_date = form.cleaned_data['e_date'].date()
            return HttpResponseRedirect(f'/litter/heatmap?start_date={start_date}&end_date={end_date}')
    else:
        form = TimeRangeForm
        if 'start_date' in request.GET and 'end_date' in request.GET:
            approved_instances = LitterInstance.objects.filter(approved=1, datetime__range=[request.GET['start_date'], request.GET['end_date']])
        else:
            approved_instances = LitterInstance.objects.filter(approved=1)
        for _instance in approved_instances:
            data.append([float(_instance.lat), float(_instance.lon), 1])
        
        dataJSON = dumps(data)
    
        return render(request, 'litter/heatmap.html', {'data': dataJSON,
                                                       'form': form,
                                                   'is_staff': request.user.is_staff})




