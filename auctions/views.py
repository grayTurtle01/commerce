from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Comment, User, Product, BidForm, Bid


def index(request):
    products = Product.objects.filter(is_active=True)
    
    try:
        counter = len(request.user.products.all())
    except:
        counter = 0
    
    return render(request, "auctions/index.html",{
        'products': products,
        'counter' : counter
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

@login_required(login_url='login')
def add_product(request):
    if request.method == 'GET':
        return render(request, 'auctions/add_product.html',{
            'counter': len(request.user.products.all())
        })

    if request.method == 'POST':
        name = request.POST['product_name']
        description = request.POST['description']
        initial_price = request.POST['initial_price']
        image_url = request.POST['image_url']
        creator = request.user.username
        try:
            category = request.POST['category']
        except:
            category = "Undefined"

        if image_url == "":
            image_url = "/static/auctions/images/not_available.jpg"


        product = Product(name=name, description=description, 
                          initial_price=initial_price, price=initial_price, 
                          image_url=image_url, category=category, creator=creator)
        product.save()

        return redirect('index')

@login_required(login_url='login')
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()

    return HttpResponseRedirect(reverse('show_profile', args=(product.creator,)))

@login_required(login_url='login')
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
        category = request.POST['category']

        product = Product.objects.get(pk=product_id)
        product.name = name
        product.description = description
        product.price = price
        product.image_url = image_url
        product.category = category

        product.save()
        

        return HttpResponseRedirect(reverse('show_product', args=(product_id,)))

def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    

    if request.method == 'GET':
        ### Is the product in favorites
        try:
            request.user.products.get(pk=product_id)
            is_selected = True
        except:
            is_selected = False
        

        ### Count favorites   
        try:
            counter = len(request.user.products.all())
        except:
            counter = 0

        
        return render(request, 'auctions/product.html', {
            'product' : product,
            'counter' : counter,
            'message': '',
            'comments': Comment.objects.filter(product_id=product_id),
            'is_selected': is_selected,
            'form': BidForm(),
            'bids': Bid.objects.filter(product_id=product_id).count()
        })

    
    ## Bid
    if request.method == 'POST':
        new_price = int(request.POST['new_price'])
        
        if product.winner == "" and new_price >= product.initial_price:
            product.price = new_price
            product.winner = request.user.username
            product.save()

            bid = Bid(new_price=new_price, bidder=request.user, product_id=product_id)
            bid.save()

            return render(request, 'auctions/product.html',{
                'product': product,
                'messageSuccess': "The Bid was accepted !!",
                'form': BidForm(),
                'comments': Comment.objects.filter(product_id=product_id),
                'counter': len(request.user.products.all()),
                'bids': Bid.objects.filter(product_id=product_id).count() 

            })

        elif new_price > product.price:
            product.price = new_price
            product.winner = request.user.username
            product.save()

            bid = Bid(new_price=new_price, bidder=request.user, product_id=product_id)
            bid.save()

            return render(request, 'auctions/product.html',{
                'product': product,
                'messageSuccess': "The Bid was accepted !!",
                'form': BidForm(),
                'comments': Comment.objects.filter(product_id=product_id),
                'counter': len(request.user.products.all()),
                'bids': Bid.objects.filter(product_id=product_id).count()

            })

        else:
            return render(request, 'auctions/product.html',{
                'product': product,
                'messageFail': f"The bid must be greater than ${product.price}",
                'form': BidForm(),
                'comments': Comment.objects.filter(product_id=product_id),
                'counter': len(request.user.products.all()),
                'bids': Bid.objects.filter(product_id=product_id).count()
            }
            )



def show_profile(request, creator):
    products = Product.objects.filter(creator=creator)

    if request.user.is_authenticated:
        counter = len(request.user.products.all())
    else: 
        counter = 0

    return render(request, 'auctions/profile.html',{
        'creator': creator,
        'products': products,
        'counter' : counter 
    })

@login_required(login_url='login')
def close_bid(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.is_active :
        product.is_active = False
    else: 
        product.is_active = True

    product.save()

    #return redirect('index')
    return HttpResponseRedirect(reverse('show_product', args=(product_id,)))

@login_required(login_url='login')
def add_book_watchlist(request, product_id):

    
    ## remove product from watchlist
    try:
        product = request.user.products.get(pk=product_id)
        product.users.remove( request.user )

    ## add product
    except:
        product = Product.objects.get(pk=product_id)
        product.users.add(request.user)
    
    return HttpResponseRedirect(reverse('show_product', args=(product_id,)))

@login_required(login_url='login')
def show_watchlist(request):
    products = request.user.products.all()
    return render(request, 'auctions/watchlist.html',{
        'products': products,
        'counter': len(request.user.products.all())
    })

@login_required(login_url='login')
def add_comment(request, product_id):
    if request.method == 'POST':
        comment = request.POST['comment']
        creator = request.user.username

        new_comment = Comment(comment=comment, creator=creator, product_id=product_id)
        new_comment.save()
    
        return HttpResponseRedirect(reverse('show_product', args=(product_id,)))

    else:
        return redirect('index')


def products_filtered(request, category):
    if category == 'All':
        products = Product.objects.all()
    elif category == 'Closed':
        products = Product.objects.filter(is_active=False)
    else:
        products = Product.objects.filter(category=category)

    if request.user.is_authenticated:
        counter = len(request.user.products.all())
    else:
        counter = 0

    return render(request, 'auctions/products_filtered.html',{
        'products': products,
        'category': category,
        'counter': counter
    })

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