from django.db import models
from django import forms
from django.forms import ModelForm, widgets
from .models import Event

Events = Event.objects.all()
venues = Events.order_by('venue').values('venue').distinct()
venue_choices = [("all", "Select All")]
for venue in venues:
    venue_choices += [(list(venue.values())[0], list(venue.values())[0])]
sort = [("date", "Date"),
        ("event", "Event"),
        ("instructor", "Instructor"),
        ("venue", "Venue"),]
order = [("ascending", "Ascending"),
         ("descending", "Descending")]

class Request(models.Model):
    venue = models.CharField(max_length=255, default="all")
    start = models.DateField(verbose_name="From:", default="2022-07-12")
    end = models.DateField(verbose_name="To:", default="2022-07-18")
    sort = models.CharField(max_length=10, default="date")
    order = models.CharField(max_length=10, default="ascending")
    date_created = models.DateTimeField(auto_now_add=True)

class EntryForm(ModelForm):
    class Meta:
        model = Request
        fields = ['venue', 'start', 'end', 'sort', 'order']
        widgets = {
            'venue': forms.CheckboxSelectMultiple(choices=venue_choices),
            'start': widgets.DateInput(attrs={'type': 'date'}),
            'end': widgets.DateInput(attrs={'type': 'date'}),
            'sort': forms.Select(choices=sort),
            'order': forms.Select(choices=order),
        }

