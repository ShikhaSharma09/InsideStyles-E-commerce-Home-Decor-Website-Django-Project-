from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Contact
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


def home(request):
 return render(request, 'app/home.html')


class Sofa1DetailView(View):
 def get(self, request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/Sofa1detail.html',
    {'product':product})
 
class LampsDetailView(View):
 def get(self, request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/Lampsdetail.html',
    {'product':product})

class KitchenDetailView(View):
 def get(self, request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/Kitchendetail.html',
    {'product':product})

class KidsDetailView(View):
 def get(self, request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/Kidsdetail.html',
    {'product':product})
 
class IndoorPlantDetailView(View):
 def get(self, request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/IndoorPlantdetail.html',
    {'product':product})
 
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  Cart(user=user, product=product).save()
  return redirect('/cart')

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user] 
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount})
    else:
      return render(request, 'app/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'amount': amount,
      'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def Sofa(request, data=None):
 if data == None:
    sofas = Product.objects.filter(category='SF')
    return render(request, 'app/Sofa.html', {'sofas':sofas})

def Lamps(request, data=None):
 if data == None:
    lamp = Product.objects.filter(category='LM')
    return render(request, 'app/Lamps.html', {'lamp':lamp})
 
def Kitchen(request, data=None):
 if data == None:
    kitchen = Product.objects.filter(category='KT')
    return render(request, 'app/Kitchen.html', {'kitchen':kitchen})
 
def Kids(request, data=None):
 if data == None:
    kid = Product.objects.filter(category='KD')
    return render(request, 'app/Kids.html', {'kid':kid})
 
def IndoorPlants(request, data=None):
 if data == None:
    plant = Product.objects.filter(category='IP')
    return render(request, 'app/Indoor_plants.html', {'plant':plant})
 
class CustomerRegistrationView(View):
  def get(self, request):
   form = CustomerRegistrationForm()
   return render(request, 'app/customerregistration.html', {'form':form})
  def post(self, request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
     messages.success(request, 'Congratulations!! Registered Successfully')
     form.save()
    return render(request, 'app/customerregistration.html',
    {'form': form})

def Signout(request):
 logout(request)
 messages.success(request, "Logged Out Successfully!")
 return redirect('login')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home') 

def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount
  return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    
    # Check if custid is provided
    if not custid:
        return HttpResponse("Customer ID is missing.")
    
    try:
        # Attempt to get the customer by custid
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        return HttpResponse("Customer does not exist.")
    
    # Proceed with order placement
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Create an order and delete the cart item
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    
    return redirect("contactus")


class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
  
  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr, name=name,locality = locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request, 'Congratulations!! Profile Updated Successfully')
    return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
 
def Contact_Us(request):
  if request.method=="POST":
    contact = Contact()
    name = request.POST.get('name')
    email = request.POST.get('email')
    number = request.POST.get('number')
    feedback = request.POST.get('feedback')
    contact.name=name
    contact.email=email
    contact.number=number
    contact.feedback=feedback
    contact.save()
  return render(request, 'app/contact_us.html')
