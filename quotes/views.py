# quotes/views.py
from django.shortcuts import render

from django.http import HttpRequest, HttpResponse

import time
import random
# Create your views here.

QUOTES = [
    "A man paints with his brains and not with his hands",
    "Genius is eternal patience",
    "If people knew how hard I worked to get my mastery, it wouldn't seem so wonderful at all",
]
IMAGES = [
    "../static/michelangelo_1.jpg",
    "../static/michelangelo_22.jpg",
    "../static/michelangelo_3.jpg",
]

def quote(request):
    """ Takes an http request as input and redirects
    to the quote of the day or home page of the quotes 
    website
    """

    template_name = 'quotes/quote.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }
    return render(request, template_name, context)



def show_all(request):
    """ Takes an http request as input and redirects
    to the show_all page of the quotes website
    """
    
    template_name = 'quotes/show_all.html'

    context = {
        "time": time.ctime(),
        "quotes": QUOTES,
        "images": IMAGES,
    }
    return render(request, template_name, context)



def about(request):
    """ Takes an http request as input and redirects
    to the about page of the quotes website
    """
    template_name = 'quotes/about.html'

    context = {
            "time": time.ctime(),
            "quotes": QUOTES,
            "images": IMAGES,
        }

    return render(request, template_name, context)
