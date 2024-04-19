from django.db import models

# Create your models here.
class Event(models.Model):
    #Fields
    node_id = models.CharField(verbose_name = "ID", max_length=3)
    node_loc = models.CharField(verbose_name = "Location", max_length=10)
    temp = models.DecimalField(verbose_name = "Temperature", max_digits=5, decimal_places=1)
    hum = models.DecimalField(verbose_name = "Humidity", max_digits=5, decimal_places=1)
    light = models.DecimalField(verbose_name = "Light Intensity", max_digits=5, decimal_places=0)
    snd = models.DecimalField(verbose_name = "Sound Level", max_digits=5, decimal_places=0)
    date_created = models.DateTimeField(verbose_name = "Date Created", auto_now_add=True)
    
    #Methods
    def __str__(self):
        return 'Event #{}'.format(self.id)