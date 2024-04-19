from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from iot.models import Event
from django.db.models import Avg, Max, Min
import datetime

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def temp_data(request):
    events = Event.objects.order_by('-date_created')[:1000]
    data = serializers.serialize('json', events) #Translating Django models into JSON formats
    return JsonResponse(data, safe=False) #Returns a string that contains an array object

def summary(request):
    Events = Event.objects.all()
    events = Events.values('node_id', 'node_loc').annotate(max_temp = Max('temp'), min_temp = Min('temp'), avg_temp = Avg('temp'), last_updated = Max('date_created'))
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'dashboard/summary.html', context) # Pass the context to HTML template