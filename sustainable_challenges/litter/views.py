from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import LitterInstance
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import InstanceForm

class LatestView(generic.ListView):
    template_name = "litter/latest.html"
    context_object_name = "latest_instance_list"

    def get_queryset(self) -> QuerySet[Any]:
        valid_instances = LitterInstance.objects.filter(approved=False)
        return valid_instances.order_by("-datetime")[:5]
    
def instance(request, instance_id):
    _instance = get_object_or_404(LitterInstance, pk=instance_id)
    return render(request, "litter/instance.html", {"instance": _instance})

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

    return render(request, 'litter/report.html', {'form': form, 'submitted': submitted, 'id': id})