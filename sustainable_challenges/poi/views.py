from typing import Any
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseForbidden
from .models import PlaceOfInterest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
#from .forms import InstanceForm, ApproveForm, TimeRangeForm
from json import dumps

# Create your views here.

