from django.db import models

from django.core.exceptions import ValidationError
from med.models import Modality
#import med

# Create your models here.

TCP_PROTOCOL = 0
UDP_PROTOCOL = 1
PROTOCOL_CHOICES = (
    (TCP_PROTOCOL, 'TCP'),
    (UDP_PROTOCOL, 'UDP'),
)
PROTOCOL_DICT = dict(PROTOCOL_CHOICES)

OUTBOUND_DIRECTION = 0
INBOUND_DIRECTION = 1

DIRECTION_CHOICES = (
    (INBOUND_DIRECTION, 'Inbound from Customer'),
    (OUTBOUND_DIRECTION, 'Outbond to Customer'),
)

UP_ACTIVE_STATE = 0
UP_IDLE_STATE = 1
DOWN_STATE = 2
DOWN_NEGOTIATING_STATE = 3
UP_NO_IKE_STATE = 4

STATE_CHOICES = (
    (UP_ACTIVE_STATE, 'UP-ACTIVE'),
    (UP_IDLE_STATE, 'UP-IDLE'),
    (DOWN_STATE, 'DOWN'),
    (DOWN_NEGOTIATING_STATE, 'DOWN-NEGOTIATING'),
    (UP_NO_IKE_STATE, 'UP-NO-IKE'),
)

class InsitePort(models.Model):
    
    name = models.CharField(max_length=32) # Name of port (FTP, telnet, ...)
    modality = models.ManyToManyField(Modality) # Modality for which this port is checked (different port sets are used for different modalities)
    direction = models.PositiveIntegerField(choices=DIRECTION_CHOICES) # Inbounding or outbounding port
    closed = models.BooleanField(default=False) # Normal status of port (for outbounding port) and any for inbounding. For example, port 5900 is closed normally. It should be opened before test
    protocol = models.PositiveIntegerField(choices=PROTOCOL_CHOICES) # TCP/UDP
    number = models.PositiveIntegerField() # Port number (21, 23, ...)
    destination = models.IPAddressField(default='0.0.0.0') # Destination Address (for inbounding port) and any address for outbounding port. For example, 443 port is opened on 150.2.101.24

    def clean(self):
        if self.destination == '0.0.0.0' and self.direction == INBOUND_DIRECTION:
            raise ValidationError('Destination address is necessary for inbounding port')
    
    def __str__(self):
        return '%s[%s]' % (self.name, self.number, )
        
    class Meta:
        ordering = ['name', ]     

class Server(models.Model):

    name = models.CharField(max_length=32, unique=True) # Name of server (olc12, ...)
    address =  models.IPAddressField() # IP address which is used to communicate between user-orientated server and primary server
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name',]
        


