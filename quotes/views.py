# quotes/views.py
from django.shortcuts import render

from django.http import HttpRequest, HttpResponse

import time
import random
# Create your views here.

quotes_list = []
images_list = []

def quote(request):

    template_name = 'quotes/quote.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        # "letter1": chr(random.randint(65,90)),
        # "letter2": chr(random.randint(65,90)),
        # "number": random.randint(1,10),
    }
    return render(request, template_name, context)



def show_all(request):
    return HttpResponse("Hello, show_all!")



def about(request):
    return HttpResponse("Hello, about!")
