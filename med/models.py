from django.db import models
import net

# Create your models here.

class Modality(models.Model):

    name = models.CharField(max_length=8, unique=True) # Name of Modality (CT, MR, VA, ...)

    def get_insite_ports(self):
        from net.models import InsitePort
        from net.models import INBOUND_DIRECTION, OUTBOUND_DIRECTION
        inbounding = InsitePort.objects.filter(direction=INBOUND_DIRECTION, modality=self).all()
        outbounding = InsitePort.objects.filter(direction=OUTBOUND_DIRECTION, closed=False, modality=self).all()
        closed = InsitePort.objects.filter(direction=OUTBOUND_DIRECTION, closed=True, modality=self).all()
        return inbounding, outbounding, closed
    
    def __str__(self):
        return self.name
