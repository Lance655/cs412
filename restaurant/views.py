# restaurant/views.py
# view functions to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse

import time
import random

DAILY_SPECIAL = [
    "Buffalo Bites", "Mac and Cheese Balls"
    "Crispy Crab Wontons", "Chicken Taquitos"
]

# Create your views here.
def main(request):
    '''Show the main page to the user.'''

    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    '''The view for the ordering page. Also creates a daily special 
    item as a context variable
    '''

    context = {
        "special": random.choice(DAILY_SPECIAL),
    }

    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def confirmation(request):
    '''Process the submission of an order and display a 
    confirmation page.'''

    if (request.POST): 

        # extract form fields into variables:
        food_item_1 = request.POST['food_item_1']
        food_item_2 = request.POST['food_item_2']
        food_item_3 = request.POST['food_item_3']
        food_item_4 = request.POST['food_item_4']
        
        context = {
            "food_item_1": food_item_1,
            "food_item_2": food_item_2,
            "food_item_3": food_item_3,
            "food_item_4": food_item_4,
            # "total": total
        }
        template_name = "restaurant/confirmation.html"
        return render(request, template_name, context)

    

    template_name = "restaurant/order.html"
    return render(request, template_name)
