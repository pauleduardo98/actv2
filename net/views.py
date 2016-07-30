from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import ipaddress
from django.db import transaction
import json
from net import *
import socket, ssl

from django.template import RequestContext
import re
import subprocess
from datetime import datetime, timedelta
import calendar
from django.contrib.auth.decorators import login_required
import math
from templates.templatetags.tags import *
from django.shortcuts import get_object_or_404

# Create your views here.


def connect(request, input):
    account = request.account
    role = account.role
    service = role.service
    
    #log = ServiceLog(account=account, service=service)
    #log.save()        
        
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
    except:
        raise Exception('Unable to create socket to connect to Primary Server')
    try:
        ssl_sock = ssl.wrap_socket(s, ca_certs=service.cert_filename, cert_reqs=ssl.CERT_REQUIRED)
    except:
        s.close()
        raise Exception('Wrong certificate')
    try:
        
        #log.start = datetime.now()
        #log.input = input
        #log.save()
    
        print(input)
    
        ssl_sock.connect((service.server.address, service.port))
        ssl_sock.write(input.encode('utf-8'))
        out = ssl_sock.read().decode('utf-8')
        ssl_sock.close()

        #log.end = datetime.now()
        #log.output = out
        #log.save()
        
        print(out)
        
    except socket.error:
        ssl_sock.close()
        raise Exception('Unable to connect to Primary Server')
    try:
        out = json.loads(out)
        error = out['error']
        answer = out['answer']
    except:
        raise Exception('Invalid format of internal data')
    if error:
        raise Exception(answer)
    return answer




def pinger_view(request):
    if request.method == 'POST':
        msg = ''
        result = 1
        try:
            address = request.POST['address']
            if int(address):
                try:
                    address = ipaddress.ip_address(request.POST['input'].strip())
                except:
                    raise Exception('Wrong IP Address format')
            else:
                system_id = request.POST['input'].strip()
                try:
                    ds = DatastoreFile.objects.all()[0]
                except:
                    raise Exception('There is no information about systems id and their nat ip addresses')
                address = ds.get_nat_ip_address_for_system_id(system_id)
            input = json.dumps({'cmd': 'ping', 'param': {'address': str(address)}})
                
            out = connect(request, input)

            if out == 1:
                msg = "Pinged"
                result = 0
            else:
                msg = "Not Pinged"
                result = 1
        except Exception as ex:
            x = ex.args
            if x:
                msg = x[0]
            else:
                msg = 'Please contact administrator'
            result = 1   
        context = { 
            'result':result, 
            'message': msg, 
        }
        return HttpResponse(json.dumps(context), content_type='application/javascript') 
    context = { 'id':'pinger', }
    return render_to_response('pinger.html', context, context_instance=RequestContext(request))
