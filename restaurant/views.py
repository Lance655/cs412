# restaurant/views.py
# view functions to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse

import time
import random

# daily special items list
DAILY_SPECIAL_LIST = [
    "Buffalo Bites", 
    "Mac and Cheese Balls",
    "Crispy Crab Wontons",
    "Chicken Taquitos",
]

# daily special dictionary
DAILY_SPECIAL_DICT = {
    "Buffalo Bites": 12.99,
    "Mac and Cheese Balls": 12.99,
    "Crispy Crab Wontons": 10.99,
    "Chicken Taquitos": 8.99
}

# normal menu items
MENU_ITEMS = {
    "Chicken Madeira": 12.99,
    "Chicken and Shrimp Gumbo": 14.99,
    "Jambalaya": 13.99,
    "Crispy Chicken Caesar Salad": 11.99,
    "Extra Chicken": 5.99,
    "Extra Shrimp": 8.99,
}

# Create your views here.
def main(request):
    '''Show the main page to the user.'''

    context = {
        "time": time.ctime(),
    }

    template_name = 'restaurant/main.html'
    return render(request, template_name, context)

def order(request):
    '''The view for the ordering page. Also creates a daily special 
    item as a context variable
    '''

    # extract the daily special and price into context variables
    special_item, special_item_price = random.choice(list(DAILY_SPECIAL_DICT.items()))

    context = {
        "special_item": special_item,
        "special_item_price": special_item_price,
        "time": time.ctime(),
    }

    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def confirmation(request):
    '''Process the submission of an order and display a 
    confirmation page.'''

    if (request.POST): 

        ordered_items = []
        total_price = 0

        # Check which items were selected and add to order
        for item, price in MENU_ITEMS.items():
            if request.POST.get(item):  # Checkbox was checked
                ordered_items.append({"name": item, "price": price})
                total_price += price
        
        # Add the daily special price
        for item, price in DAILY_SPECIAL_DICT.items():
            if request.POST.get(item):
                ordered_items.append({"name": item, "price": price})
                total_price += price

        # Get the customer information
        customer_name = request.POST.get("name", "")
        customer_phone = request.POST.get("phone", "")
        customer_email = request.POST.get("email", "")


        # Generate the expected ready time (30-60 minutes from now)
        wait_time = random.randint(30, 60)  # Random minutes
        ready_timestamp = time.time() + (wait_time * 60)  # Convert to seconds

        # current_time = time.strftime("%I:%M %p", time.localtime())

        # print("Current Time:", current_time)
        # print("local time:", time.localtime())

        # ready_time = time.ctime(ready_timestamp)

        ready_time = time.strftime("%I:%M %p", time.localtime(ready_timestamp))  # Format time

        # Extract the special instructions
        special_instructions = request.POST.get("special_instructions", "")


        # context variables
        context = {
            "ordered_items": ordered_items,
            "total_price": total_price,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "ready_time": ready_time,
            "time": time.ctime(),
            "special_instructions": special_instructions,
        }

        template_name = "restaurant/confirmation.html"
        return render(request, template_name, context)



    # make sure if its a get request, it has the needed context variables
    special_item, special_item_price = random.choice(list(DAILY_SPECIAL_DICT.items()))

    context = {
        "special_item": special_item,
        "special_item_price": special_item_price,
        "time": time.ctime(),
    }

    # send the user back to the order page if a get request
    template_name = "restaurant/order.html"
    return render(request, template_name, context)
