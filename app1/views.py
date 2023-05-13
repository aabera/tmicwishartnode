from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, UserProfile
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_countries import countries
import json


def login_view(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')

        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            response = HttpResponse()
            response.delete_cookie('register')  # delete the cart cookie
            login(request, user)
            response = HttpResponse()
            response.set_cookie('cart', json.dumps(cart), max_age=3600 * 24 * 30)  # set a cookie that lasts for 30 days
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # session expires when user closes browser
            return redirect('app1:home')  # replace 'home' with the name of your home page URL
        else:
            error_message = 'Invalid email or password'
    else:
        error_message = None
    return render(request, 'app1/checkout.html', {'error_message': error_message})

def registration(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        company_name = request.POST.get('company_name', '')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        e_mail = request.POST.get('e_mail')
        account = request.POST.get('account')
        order_note = request.POST.get('order_note')
        password = request.POST.get('password')

        data = {
            'f_name': f_name,
            'l_name': l_name,
            'company_name': company_name,
            'country': country,
            'address': address,
            'city': city,
            'province': province,
            'postal_code': postal_code,
            'phone': phone,
            'e_mail': e_mail,
            'order_note': order_note,
        }
        # Create user if account is checked
        if account:
            user = User.objects.create_user(
                username=e_mail,
                password=password,  # set a default password here or let the user set it later
                email=e_mail,
                first_name=f_name,
                last_name=l_name,
            )
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                company_name=company_name,
                order_note=order_note,
                country=country,
                address=address,
                city=city,
                province=province,
                postal_code=postal_code,
                phone=phone
            )
            user_profile.save()
            # This functions takes the user details and saves the order in the db and send email to admin and user.
            response = redirect('app1:success_order')
            response.set_cookie('register', json.dumps(data), expires=datetime.datetime.now() + datetime.timedelta(days=1))
            return response
        else:
            response = redirect('app1:success_order')
            response.set_cookie('register', json.dumps(data), expires=datetime.datetime.now() + datetime.timedelta(days=1))
            return response
    else:
        return redirect('app1:checkout')

def index(request):
    return render(request, 'app1/index.html')

def our_process(request):
    return render(request, 'app1/our_process.html')

def fund(request):
    return render(request, 'app1/funding_sources.html')

def about(request):
    return render(request, 'app1/about.html')

def equipment(request):
    return render(request, 'app1/equipment.html')

def opportunity(request):
    return render(request, 'app1/opportunities.html')

def services(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'app1/services.html', context)

class SelectOption(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'app1/select-option.html'

def checkout(request):
    country_choices = [(code, name) for code, name in countries]
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    order_items = []
    total = 0
    for item_id, item_data in cart.items():
        item = Item.objects.filter(id=item_data['item_id']).first()
        if item:
            item_orders = {}
            item_orders["image"] = item.image
            item_orders["title"] = item.title
            item_orders["classification"] = item_data['classification']
            item_orders["item_id"] = item_data['item_id']
            item_orders["quantity"] = item_data['quantity']
            item_orders["price"] = item_data['price']
            item_orders["sub_total"] = item_orders["quantity"] * item_orders["price"]
            order_items.append(item_orders)
            total += item_orders["sub_total"]
    context = {
        'object': order_items,
        'total': total,
        'country_choices': country_choices,
    }
    return render(request, 'app1/checkout.html', context)

def our_process(request):
    return render(request, 'app1/our_process.html')

# Cart Items
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        cart = json.loads(self.request.COOKIES.get('cart', '{}'))
        order_items = []
        total = 0
        for item_id, item_data in cart.items():
            item = Item.objects.filter(id=item_data['item_id']).first()
            if item:
                item_orders = {}
                item_orders["image"] = item.image
                item_orders["title"] = item.title
                item_orders["classification"] = item_data['classification']
                item_orders["item_id"] = item_data['item_id']
                item_orders["analysis"] = item_data['analysis']
                item_orders["sample"] = item_data['sample']
                item_orders["quantity"] = item_data['quantity']
                item_orders["price"] = item_data['price']
                item_orders["sub_total"] = item_orders["quantity"] * item_orders["price"]
                order_items.append(item_orders)
                total += item_orders["sub_total"]
        context = {
            'object': order_items,
            'total': total,
        }
        print(order_items)
        return render(self.request, 'app1/add-to-cart.html', context)

# Complete checkout and send email to user and admin
def checkout_complete(request):
    # function to populate user details to email
    if not request.user.is_authenticated:
        # Get the cookie value from the request
        cookie_value = request.COOKIES.get('register')
        # Parse the cookie value into a dictionary
        data = json.loads(cookie_value)
        # Get the email address from the dictionary
        email = data.get('e_mail')
    else:
        print("Helloooooooooo")
        user = request.user
        email = user.email

        #Get the user profile based on the email
        profile = UserProfile.objects.get(user__email=email)
        print("This is my profile", profile)
        # Populate the data dictionary with the profile fields
        data = {
            'f_name': user.first_name,
            'l_name': user.last_name,
            'company_name': profile.company_name,
            'country': profile.country,
            'address': profile.address,
            'city': profile.city,
            'province': profile.province,
            'postal_code': profile.postal_code,
            'phone': profile.phone,
            'e_mail': email,  # use the email from user
        }
    # Cookie exists, do something here
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    order_items = []
    for key, value in cart.items():
        item_id, classification = key.split("_")
        item = get_object_or_404(Item, pk=item_id)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=email,
            ordered=False,
            quantity=value['quantity'],
            category=value['classification'],
            sample_type=value['sample'],
            analysis_type=value['analysis'],
            sub_total=value['quantity'] * value["price"]
        )
        if created:
            order_items.append(order_item)
    if order_items:
        order = Order.objects.create(user=email, total=0)
        order.items.add(*order_items)
        total = 0
        for order_item in order_items:
            total += order_item.sub_total
            order_item.ordered = True
            order_item.save()
        order.ordered = True
        order.total = total
        order.save()

        items = order.items.all()
        order_itemss = []
        # Do something with the items
        for item in items:
            cart = {}
            cart["product"] = item.item.title
            cart["quantity"] = item.quantity
            cart["category"] = item.category
            cart["slug"] = item.item.slug
            cart["total"] = item.sub_total
            order_itemss.append(cart)
        context = {
            "object": order_itemss,
            "total": order.total,
            "date": order.ordered_date,
            "order_id": order.id,
            "data": data
        }
        # send email
        subject = f'Your TMIC Wishart Node order #{order.id} has been received'
        to_email = [email]
        from_email = settings.DEFAULT_FROM_EMAIL
        # Render the HTML email template
        html_content = render_to_string('app1/order_email.html', context)
        # Create the email message object
        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        # Add the admin email as a bcc recipient
        admin_email = settings.ADMIN_EMAIL
        if admin_email:
            msg.bcc = [admin_email]
        # Send the email
        msg.send()
        response = redirect('app1:finish_checkout')
        response.delete_cookie('cart')
        response.set_cookie('order', order.id, expires=datetime.datetime.now() + datetime.timedelta(days=1))
        if 'register' in request.COOKIES:
            response.delete_cookie('register')
        return response
    return redirect('app1:services')

def opportunity(request):
    return render(request, 'app1/opportunities.html')


def learn(request):
    return render(request, 'app1/learn.html')


def database(request):
    return render(request, 'app1/database.html')


def software(request):
    return render(request, 'app1/web_servers.html')


def research(request):
    return render(request, 'app1/research_hotel.html')


def FAQ(request):
    return render(request, 'app1/FAQ.html')


def testimonials(request):
    return render(request, 'app1/testimonials.html')


def awards(request):
    return render(request, 'app1/awards.html')


def quality(request):
    return render(request, 'app1/quality.html')


def news(request):
    return render(request, 'app1/news.html')


def spinoff(request):
    return render(request, 'app1/spinOffs.html')

def workshop(request):
    return render(request, 'app1/workshop.html')


def metabolomics(request):
    return render(request, 'app1/metabolomics.html')


@xframe_options_exempt
@csrf_exempt
def videos(request):
    return render(request, 'app1/videos.html')


def impact(request):
    return render(request, 'app1/impact.html')


def publications(request):
    return render(request, 'app1/publications.html')

def contact(request):
    return render(request, 'app1/contact.html')

def finish_checkout(request):
    if 'order' not in request.COOKIES:
        return redirect('app1:services')
    order = json.loads(request.COOKIES.get('order', '{}'))
    orders = Order.objects.get(id=int(order))
    # Get all the items in the order
    items = orders.items.all()
    order_items = []
    # Do something with the items
    for item in items:
        cart = {}
        cart["product"] = item.item.title
        cart["quantity"] = item.quantity
        cart["category"] = item.category
        cart["slug"] = item.item.slug
        cart["total"] = item.sub_total
        order_items.append(cart)
    context = {
        "object": order_items,
        "total": orders.total,
        "date": orders.ordered_date,
        "order_id": order
    }
    # response = render(request, 'app1/order_email.html', context)
    response = render(request, 'app1/success_order.html', context)
    return response
