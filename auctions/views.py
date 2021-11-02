from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Product, Foo


def index(request):
    products = Product.objects.all()
    return render(request, "auctions/index.html",{
        'products': products,
        'counter': 0
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_product(request):
    if request.method == 'GET':
        return render(request, 'auctions/add_product.html')

    if request.method == 'POST':
        name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        image_url = request.POST['image_url']
        category = request.POST['category']
        creator = request.user

        product = Product(name=name, description=description, price=price, 
                          image_url=image_url, category=category, creator=creator)
        product.save()

        return redirect('index')

def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()

    return redirect('index')

def edit_product(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(pk=product_id)
        return render(request, 'auctions/edit_product.html', {
            'product' : product
        })

    if request.method == 'POST':
        name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        image_url = request.POST['image_url']
        #image_url = f"auctions/images/{image}"
        category = request.POST['category']

        product = Product.objects.get(pk=product_id)
        product.name = name
        product.description = description
        product.price = price
        #product.image = image
        product.image_url = image_url
        product.category = category

        product.save()
        

        return redirect('index')

def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'auctions/product.html', {
        'product' : product,
        'counter': 0
    })


def add_book_watchlist(request):

    return redirect('index')


from .models import UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_file(request.FILES['file'], request.POST['title'])
            return redirect('index')
        else:
            return render(request, 'auctions/upload.html', {
                'form': form
            })
        
    

    if request.method == 'GET':
        form = UploadFileForm()
        return render(request, 'auctions/upload.html',{
            'form': form
        })

import os
def handle_upload_file(f, title):
    
    directory = os.getcwd()
    full_path = directory + f"/auctions/static/auctions/images/{title}.jpg"

    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)