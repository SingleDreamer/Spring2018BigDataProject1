# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect

#from django.db import connection

from models import Gene

import csv
from adkbase_program import adkbase_django as adk

# Create your views here.

from django.http import HttpResponse

def reset(request):
    adk.reset()
    print "done"
    return redirect('index')

def index(request):
    return render(request, 'adkbase/search_form.html')


def search(request):
    message = ""
    output = ""
    #adk.start()
    #adk.reset_sql()
    if 'i' in request.GET:
        message = 'Your command was: %r' % request.GET['c'].encode("utf-8")
        message += '<br />Your input was %r' % request.GET['i'].encode("utf-8")
        if request.GET['c'] == '1':
            output = adk.get_c1(request.GET['i']).encode("utf-8")
        elif request.GET['c'] == '2':
            output = adk.get_c2(request.GET['i']).encode("utf-8")
        elif request.GET['c'] == '3':
            output = adk.get_c3(request.GET['i']).encode("utf-8")
        elif request.GET['c'] == '4':
            output = adk.get_c4(request.GET['i']).encode("utf-8")
    else:
        message = 'You submitted an empty form.'
    message += '<br /><br />' + output
    message += '<p/>    <a class="btn btn-default" href="/adkbase/" role="button"><button>return</button></a>'
    #adk.terminate(True)
    return HttpResponse(message)
