from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms 
from django.contrib.auth.decorators import login_required

from .models import User, NewListing, Bid, Watchlist, Comment, ClosedListing


def index(request):
    content = NewListing.objects.all()
    return render(request, "auctions/index.html",{
        "content":content 
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

#Creating a new listing: 
class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=120)
    bid = forms.IntegerField()
    image = forms.URLField(required=False)
    category = forms.CharField(required=False)

@login_required(login_url="login")
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            #Get the data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = Bid(bid_value=int(form.cleaned_data["bid"]))
            bid.save()
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            #Get the username of user posting the data:
            owner = request.user.get_username()      
            
            #Pass the data to the NewListing model to ba saved in database
            listing = NewListing(title=title, description=description,
            bid=bid, image=image, category=category, owner=owner )
            listing.save()
            
            return redirect("index")

    return render(request, "auctions/newlisting.html",{
        "form": NewListingForm().as_p()
    }) 

@login_required(login_url="login")
def listing(request, listing_id):
    if request.method == "GET":
        this_listing = NewListing.objects.get(pk=listing_id)
        comments = Comment.objects.filter(listing=this_listing)
        return render(request, "auctions/listing.html",{
            "this_listing":this_listing,
            "comments": comments 
        })

    elif request.method == "POST":
        user = request.user
        listing = NewListing.objects.get(pk=listing_id)
        #watchlist_item = Watchlist(user=user,listing=listing)
        try:
            w = Watchlist.objects.get(user=user, listing=listing)
            w.delete()
        except Watchlist.DoesNotExist:
            w = Watchlist(user=user, listing=listing)
            w.save()
        #watchlist_item.save()
        return redirect("index")

@login_required(login_url="login")
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html",{
        "watchlists":watchlists
    })

@login_required(login_url="login")
def comment(request, listing_id):
    if request.method == "POST":
        listing = NewListing.objects.get(pk=listing_id)
        user = request.user
        text = request.POST["comment"]
        comment = Comment(listing=listing, user=user, text=text)
        comment.save()
        return redirect("listing", listing_id=listing.id)

@login_required(login_url="login")
def newbid(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = NewListing.objects.get(pk=listing_id)
        new_value = int(request.POST["bid"])
        previous_value = listing.bid.bid_value
        #Check if bid greater than previous
        if previous_value > new_value:
            return HttpResponse("<h1>Placed bid should be greater than or equal to current bid</h1>")
        else:
            newbid = Bid(bid_value=new_value, user=user)
            newbid.save()
            listing.bid = newbid
            listing.save()
            return redirect("listing", listing_id=listing_id)
    
@login_required(login_url="login")
def category(request):
    listings = NewListing.objects.all()
    category_list = []
    for listing in listings:
        category_list.append(listing.category)
    category_set = set(category_list)
    return render(request,"auctions/categories.html",{
        "categories":category_set
    })
  
@login_required(login_url="login")
def this_category(request, category):
    content = NewListing.objects.filter(category=category)
    return render(request, "auctions/category.html",{
        "content":content 
    })

@login_required(login_url="login")
def close(request, listing_id):
    if request.method == "POST":
        listing = NewListing.objects.get(pk=listing_id)
        #Pass the closed listing to Closed listing model and delete it(inactive)
        closed_listing = ClosedListing(title=listing.title,
        description = listing.description,
        bid = listing.bid,
        image  =listing.image,
        category= listing.category,
        owner = listing.owner)
        closed_listing.save()
        listing.delete()
        return redirect("index")

@login_required(login_url="login")
def closed(request):
    content = ClosedListing.objects.all()
    return render(request, "auctions/closed.html",{
        "content":content 
    })

@login_required(login_url="login")
def closed_listing(request, listing_id):
    if request.method == "GET":
        this_listing = ClosedListing.objects.get(pk=listing_id)
        return render(request, "auctions/closed_listing.html",{
            "this_listing":this_listing
        })