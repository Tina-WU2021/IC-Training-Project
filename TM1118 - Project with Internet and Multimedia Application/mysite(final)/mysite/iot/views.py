import json
from xmlrpc.client import DateTime

from django.shortcuts import render
from . import iot_mqtt
from . import myTool
from .models import Event
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.core import serializers
from datetime import timezone,datetime

timezone_str = "+08:00"

# Create your views here.
def index(request):
    events = Event.objects.order_by('-date_created')[:500]
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'iot/index.html', context) # Pass the context to HTML template

def log(request):
    events = Event.objects.order_by('-date_created')[:500]
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'iot/log.html', context) # Pass the context to HTML template

def info(request):
    Events = Event.objects.all()
    events = Events.values('node_id', 'node_loc').annotate(max_temp = Max('temp'), min_temp = Min('temp'), avg_temp = Avg('temp'), last_updated = Max('date_created'))
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'iot/info.html', context) # Pass the context to HTML template

def data(request):
    return render(request, 'iot/data.html')

def hour_analysis_page(request):
    return render(request, 'iot/dataAnalysisByTimeInHour.html')

def temp_data(request):
    events = Event.objects.order_by('-date_created')[:1000]
    data = serializers.serialize('json', events) #Translating Django models into JSON formats
    return JsonResponse(data, safe=False) #Returns a string that contains an array object

def node_analysis_page(request):
    return render(request, 'iot/dataAnalysisByNode.html')

def second_analysis_page(request):
    return render(request, 'iot/dataAnalysisSecond.html')

def hour_analysis_data(request):
    data = myTool.getDataByIdInHourWithRange("2022-07-13T15:00:00.000"+timezone_str,datetime.now().isoformat(),myTool.getAllDistinceNode("2022-07-13T07:00:00.000Z",datetime.now().isoformat()))
    return JsonResponse(data, safe=False)

def second_analysis_data(request):
    data = myTool.secondAnalysis()
    return JsonResponse(data, safe=False)
    
def navbar(request):
    return render(request, 'iot/navbar.html')
    
def data_warning(request):
    return render(request, 'iot/dataWarning.html')