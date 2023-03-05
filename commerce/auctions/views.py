from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import logging

from .models import *

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "auctions/index.html", {
        "lists": List.objects.filter(is_active=True)
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


@login_required
def create_list(request):

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        list = List(title=request.POST['title'], description=request.POST['description'],
                    price=request.POST['price'], image_url=request.POST['image_url'], category=request.POST['category'])

        list.listed_by = user
        list.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create-list.html", {
        "categories": Categories
    })


message = ""


@login_required
def display_list(request, list_id):
    list = List.objects.get(pk=list_id)
    bid = Bid.objects.filter(list__title=list.title)
    comment = Comment.objects.filter(list__title=list.title)
    user = User.objects.get(username=request.user)
    watchlist = WatchList.objects.filter(list__title=list.title, user=user)

    return render(request, "auctions/list.html", {
        "list": list,
        "bid": bid.last(),
        "message": message,
        "comments": comment,
        "count": bid.count(),
        "watchlist": watchlist
    })


def place_bid(request, list_id):
    if request.method == 'POST':
        list = List.objects.get(pk=list_id)
        user = User.objects.get(username=request.user)
        bid_last = Bid.objects.filter(list__title=list.title).last()
        bid = Bid(bid=request.POST['bid'])
        logger.warning(bid_last)
        global message
        if bid_last:
            if float(bid_last.bid) >= float(bid.bid):

                message = "Your bid must be greater than the current one."
                return HttpResponseRedirect(reverse("list", args=(list_id, )))
            else:
                bid_save(list, user, bid)

        elif float(list.price) <= float(bid.bid):
            bid_save(list, user, bid)
        else:
            message = "Your bid must be greater than the current one."

    return HttpResponseRedirect(reverse("list", args=(list_id, )))


def bid_save(list, user, bid):
    global message
    bid.list = list
    bid.user = user
    bid.save()
    message = "Your bid is successfully placed."
    return HttpResponseRedirect(reverse("list", args=(list.id, )))


def comment(request, list_id):
    if request.method == 'POST':
        list = List.objects.get(pk=list_id)
        user = User.objects.get(username=request.user)
        comment = Comment(comment=request.POST['comment'])
        comment.list = list
        comment.user = user
        comment.save()
        return HttpResponseRedirect(reverse("list", args=(list.id, )))


def watch_list(request, list_id):
    if request.method == 'POST':
        list = List.objects.get(pk=list_id)
        user = User.objects.get(username=request.user)
        if request.POST.get('watchlist') == "Add to watchlist":
            watchlist = WatchList()
            watchlist.list = list
            watchlist.user = user
            watchlist.save()
        else:
            WatchList.objects.filter(
                list__title=list.title).delete()
        return HttpResponseRedirect(reverse("list", args=(list.id, )))


@login_required
def display_watchlist(request, user):
    return render(request, "auctions/watchlist.html", {
        "watchlists": WatchList.objects.filter(user__username=request.user),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories
    })


def category(request, category):
    list = List.objects.filter(category=category, is_active=True)
    return render(request, "auctions/display-categories.html", {
        "lists": list,
        "category": category
    })


def close_list(request, list_id):
    if request.method == "POST":
        list = List.objects.get(pk=list_id)

        list.is_active = False
        list.save()
        return HttpResponseRedirect(reverse("index"))


@login_required
def display_closed_list(request):
    list = List.objects.filter(is_active=False)
    return render(request, "auctions/close-list.html", {
        "lists": list,
    })


def result(request, list_id):
    list = List.objects.get(pk=list_id)
    bid = Bid.objects.filter(list__title=list.title).last()
    return render(request, "auctions/result.html", {
        "list": list,
        "bid": bid
    })
