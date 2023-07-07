from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
import uuid

from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/home.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Retrieve cart data
    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'store/product_detail.html', {'product': product, 'cartItems': cartItems})




def register(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            # ... Get other form data

            # Generate a unique username using uuid
            username = str(uuid.uuid4())

            # Create a new User object with the provided username
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create a new Customer object and associate it with the user
            customer = Customer(user=user, name=name, email=email)
            # ... Set other attributes of the customer object

            # Save the customer object
            customer.save()

            # Return a JSON response indicating successful registration
            return JsonResponse({'success': True})
        except Exception as e:
            # Print the exception message for debugging
            print(e)

            # Return a JSON response with an error message
            return JsonResponse({'success': False, 'error': 'Registration failed. Please try again.'})

    # Return a JSON response with an error message for invalid request method
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def store_home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/home.html', context)





