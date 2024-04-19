from django.shortcuts import render
from .models import Event
from iot.models import Event as iot
from .forms import Request, EntryForm
from django.db.models import Avg

# Create your views here.
def index(request):
    events = Event.objects.all()
    context = {'events' : events} # Store the data in "context" dictionaries
    return render(request, 'event/index.html', context) # Pass the context to HTML template

def request(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            form.save()
            requested = Request.objects.all()
            if "all" in list(requested.values())[-1]['venue']:
                venues = "all recorded venues"
                venuelist = [venue['venue'] for venue in list(Event.objects.order_by('venue').values('venue').distinct())]
            else:
                venuelist = list(requested.values())[-1]['venue'].strip('\'][').split('\', \'')
                
                venues = ""
                if len(venuelist) > 1:
                    for i in range(len(venuelist)-2):
                        venues += venuelist[i]
                        venues += ", "
                    venues += venuelist[-2]
                    venues += " and "
                venues += venuelist[-1]

            start = list(requested.values())[-1]['start']
            end = list(requested.values())[-1]['end']
            period = {'start': start, 'end': end}

            sort = list(requested.values())[-1]['sort']
            order = list(requested.values())[-1]['order']
            if order == "descending":
                sort = "-"+sort

            Events = Event.objects.values().filter(venue__in=venuelist, date__gte = start, date__lte = end).order_by(sort)
            EnvData = iot.objects.filter(node_loc__in=[venue.upper() for venue in venuelist], date_created__date__gte=start, date_created__date__lte=end).values('node_loc').annotate(temp = Avg('temp'), hum = Avg('hum'), light = Avg('light'), snd = Avg('snd'))
            
            context = {'venues': venues, 'period': period, 'events': Events,'envdata': EnvData, 'sort': sort.strip("-"), 'order': order}
            return render(request, 'event/time-event-data.html', context)

    else:
        form = EntryForm()

    context = {'form' : form} # Store the data in "context" dictionaries
    return render(request, 'event/form.html', context) # Pass the context to HTML template
