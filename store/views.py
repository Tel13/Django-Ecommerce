from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

# pentru a aduaga multiple query in filter la cautare
from django.db.models import Q
import json
from cart.cart import Cart


def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # query the products db model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
            messages.success(request, "That product does not exist...Please try agin")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})
    

def update_info(request):
    if request.user.is_authenticated:
        #Get Current user
        current_user = Profile.objects.get(user__id=request.user.id) # ca sa ia idul de la profile model
        # Get Current users's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # get original User form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your info has been updated...")
            return redirect('home')
        return render(request, "update_info.html", {"form":form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in to acces the page...")
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated....")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else: 
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to acces the page...")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated...")

            return redirect('home')
        return render(request, "update_user.html", {"user_form":user_form})
    else:
        messages.success(request, "You must be logged in to acces the page...")
        return redirect('home')
    

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do some shoping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their save car from db
            saved_cart = current_user.old_cart
            # Convert db string to python dictionary
            if saved_cart:
                #Convert to disctionary using JSON
                converted_cart = json.loads(saved_cart)
                # add the loaded disctionary to our session
                cart = Cart(request)
                # Loop to the cart and add the items from db
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, 'You have been login')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # stergem fildurile
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Username created. Please fill out your user info below....')
            return redirect('update_info')
        else:
            messages.success(request, 'There was a problem please try again...')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    #replace hyphens with spacees
    foo = foo.replace('-', ' ')
    # grab the category from url
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, "That category dosen't exist")
        return redirect('home')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})