from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Type, Size, Topping, Order, Menu, Purchase, Product
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import stripe
import sendgrid
import os
from sendgrid.helpers.mail import *

# Get stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY

# Use SendGrid API to send email to the user after payment done
def send_email_SendGrid(user_email, message):
    sg = sendgrid.SendGridAPIClient('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')
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": "{}".format(user_email)
            }
          ],
          "subject": "Hello from the Pizza Online Order!"
        }
      ],
      "from": {
        "email": "moataz.ghobashi@gmail.com"
      },
      "content": [
        {
          "type": "text/plain",
          "value": "{}".format(message)
        }
      ]
    }
    response = sg.client.mail.send.post(request_body=data)

# Display the main page
def index(request):
    # Check if the user authenticated
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":"Please Login"})

    # Get the product and category
    products = Product.objects.all()
    category = Type.objects.all()
    # Get the food and price and update the Order table
    if request.method == "POST":
        food = request.POST['name']
        price = request.POST['price']
        item_type = Type.objects.get(name='Popular')
        cart = Order(item=food, user=request.user, price=price, type=item_type)
        cart.save()
        return HttpResponseRedirect(reverse("index"))

    context = {
        'category': category,
        'products': products
    }
    return render(request, "orders/index.html", context)

# Menu view that display the Menu based on the type
def menus(request, item_id):
    items = Menu.objects.filter(type=item_id)
    food = [Size.objects.filter(menu=i) for i in items]
    category = Type.objects.all()
    context = {
        'food': [i[0] for i in food],
        'toppings': Topping.objects.all(),
        'category': category,
        'item_id': item_id,
    }

    return render(request, "orders/menu.html", context)

# Function to add food item to the user's cart
def addFood(request):
    # Get the food, price, food's ID, topping_list and food Type(Menu Type)
    food = request.POST["food"]
    price = request.POST["price"]
    type = request.POST["id"]
    topping_list = request.POST.getlist("topping1")
    item_type = Type.objects.get(pk=type)

    # If the selected food is in adds-ons,
    # Then make sure the user has already ordered some food items in the Cart
    # and prevent the user from select the same add_ons more the number of ordered food item
    add_ons = ['+ Mushrooms', '+ Green Peppers', '+ Onions', 'Extra Cheese on any sub']
    if food in add_ons:
        items = Order.objects.filter(type=item_type, user=request.user)
        subs = [i.item for i in items if i.item not in add_ons]
        for add in add_ons:
            if food == add:
                extra_add = [i.item for i in items if i.item == add]
                if len(subs) <= len(extra_add):
                    return HttpResponseRedirect(reverse("index"))

    # If the user select topping or items
    # Update Order table and update the topping field
    if food in ['1 topping', '1 item', '2 toppings', '2 items', '3 toppings', '3 items', 'Special']:
        cart = Order(item=food, user=request.user, price=price, type=item_type)
        cart.save()
        for t in topping_list[0].split(','):
            a = Topping.objects.get(item=t)
            cart.topping.add(a)
    else:
        cart = Order(item=food, user=request.user, price=price, type=item_type)
        cart.save()

    return HttpResponseRedirect(reverse("index"))

# Display the cart view(Ordered food)
def carts(request):
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})

    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    context = {
        'food': shopping,
        'price': round(total_price, 2),
    }
    return render(request, "orders/payment.html", context)

# Handle the user payment and send email
def payments(request):
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})

    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    email_message = 'Please find your order below: \n\n'

    if request.method == "POST":
        # Get the token
        token = request.POST.get('token', False)
        # Use stripe api to accept the user's payment
        pay = stripe.Charge.create(
              amount=int(round(total_price, 2) * 100),
              currency="usd",
              source=token,
              description=request.user.email,
        )

        # Purchase the ordered food and update the table
        # build up the email message with each food and price
        for i in shopping:
            Purchase(order=i.item, user=request.user, price=i.price).save()
            email_message += i.item + "  " + str(i.price) + '\n'

        email_message += 'Total price is {}'.format(str(total_price))
        Order.objects.filter(user=request.user).delete()

        # Use sendgrid to send the message to the user's email
        try:
            send_email_SendGrid(request.user.email, email_message)
        except Exception as e:
            print(e)
            pass

        return HttpResponseRedirect(reverse("carts"))

# Delete food item based on its id
def delete(request, item_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})
    # Get the food and delete it
    delete_order = Order.objects.get(pk=item_id)
    delete_order.delete()

    # Get all the food item that related to subs menu
    # Then, created list with all food that not add-ons
    # And, created list with all add_ons
    # delete all add_ons food if there is no more food
    type = Type.objects.get(name='Subs')
    get_subs = Order.objects.filter(type=type.id, user=request.user)

    add_ons = ['+ Mushrooms', '+ Green Peppers', '+ Onions', 'Extra Cheese on any sub']
    items_name = [i.item for i in get_subs if i.item not in add_ons]
    extra_exsit = [i.item for i in get_subs if i.item in add_ons]

    if extra_exsit and not items_name:
        for i in extra_exsit:
            Order.objects.filter(item=i, user=request.user).delete()

    return HttpResponseRedirect(reverse("carts"))

# Register new user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if not password == password2:
            return render(request, "orders/register.html", {"message":"Passwords don't match."})

        user = User.objects.create_user(username, email, password)
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return render(request, "orders/login.html", {"message":"Registered. You can log in now."})
    return render(request, "orders/register.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    return render(request, "orders/login.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
