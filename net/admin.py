from django.contrib import admin
from net.models import *
import ipaddress

# Register your models here.

class InsitePortAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(InsitePort, InsitePortAdmin)

