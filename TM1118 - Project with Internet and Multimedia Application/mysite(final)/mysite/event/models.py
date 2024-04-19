from django.db import models

# Create your models here.
class Event(models.Model):
    #Fields
    venue = models.CharField(verbose_name = "Venue", max_length=10)
    date = models.DateField(verbose_name = "Date")
    start_time = models.TimeField(verbose_name = "Time start")
    end_time = models.TimeField(verbose_name = "Time end")
    event = models.CharField(verbose_name = "Event", max_length = 10)
    instructor = models.CharField(verbose_name = "Instructor", max_length = 20)
    
    #Methods
    def __str__(self):
        return 'Event #{}'.format(self.id)