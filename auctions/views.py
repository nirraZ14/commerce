from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Category,Comment,Bid


def index(request):
    activeListings=Listing.objects.filter(isActive= True)
    allcategories=Category.objects.all()
    
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allcategories
    })

def listing(request,id):
    listingData=Listing.objects.get(pk=id)
    isAdmin=request.user.username == listingData.owner.username
    listingInWatchlist=request.user in listingData.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "listingInWatchlist":listingInWatchlist,
        "isAdmin":isAdmin,
        "allcomments":allcomments
    })
def close(request,id):
    listingData=Listing.objects.get(pk=id)
    isAdmin=request.user.username == listingData.owner.username
    listingInWatchlist=request.user in listingData.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingData)
    listingData.isActive=False
    listingData.save()
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "listingInWatchlist":listingInWatchlist,
        "isAdmin":isAdmin,
        "allcomments":allcomments
    })


def remove(request,id):
    listingData=Listing.objects.get(pk=id)
    currenUser=request.user
    listingData.watchlist.remove(currenUser)

    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    currentUser=request.user
    listings=currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings":listings
    })

def add(request,id):
    listingData=Listing.objects.get(pk=id)
    currenUser=request.user
    listingData.watchlist.add(currenUser)

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def cAtegory(request):
    if request.method=="POST":
        categoryForm= request.POST["category"]
        category=Category.objects.get(categoryName=categoryForm)
        activeListings=Listing.objects.filter(isActive= True, category=category)
        allcategories=Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allcategories
    })

def addComment(request, id):
    currentUser=request.user
    listingData=Listing.objects.get(pk=id)
    message=request.POST['newComment']
    newComment=Comment(
        message=message,
        author=currentUser,
        listing=listingData
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def create(request):
    if request.method=="POST":

        title=request.POST.get("title")
        price=request.POST.get('price')
        description=request.POST.get('description')
        category=request.POST['category']
        User=request.user
        categoryData=Category.objects.get(
            categoryName=category
        )
        bid=Bid(bid=price, user=User)
        bid.save()
        newListing=Listing(
            title=title,
            category=categoryData,
            price=bid,
            owner=User,
            description=description
        )
        newListing.save()
        listings=Listing.objects.all()
        return render(request,"auctions/index.html",{
            "listings":listings
        })
    else:
        allCategories=Category.objects.all()
        return render(request,"auctions/create.html",{
            "categories":allCategories
        })

def addBid(request,id):
    listingData=Listing.objects.get(pk=id)
    isAdmin=request.user.username == listingData.owner.username
    currentUser=request.user
    newBid=request.POST['newBid']
    if int(newBid) > listingData.price.bid:
        updateBid=Bid(
            bid=newBid,
            user=currentUser
        )
        updateBid.save()
        listingData.price=updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "update":True,
            "message":"Successful",
            "isAdmin":isAdmin
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "update":False,
            "message":"Failed",
            "isAdmin":isAdmin
        })

def wins(request):
    listings=Listing.objects.filter(isActive=False)
    return render(request, "auctions/wins.html", {
        "listings": listings
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
