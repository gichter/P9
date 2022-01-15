from email import message
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from itertools import chain

from django.db.models import CharField, Value

from .forms import *
from .models import *

def index(request):
    return HttpResponse("index")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else: 
            messages.info(request, 'Username or Password is incorrect.')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):    
    reviews = Review.objects.all()
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.all() 
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    
    return render(request, 'reviews/dashboard.html',  context={'posts': posts})


@login_required(login_url='login')
def posts(request):
    context = {}
    return render(request, 'reviews/posts.html', context)

@login_required(login_url='login')
def subscriptions(request):
    context = {}
    return render(request, 'reviews/subscriptions.html', context)


@login_required(login_url='login')
def createTicket(request):
    form = TicketForm()    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request, 'reviews/ticket_form.html', context)


@login_required(login_url='login')
def updateTicket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    form = TicketForm(instance=ticket)    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request, 'reviews/ticket_form.html', context)


def deleteTicket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('/')
    context = {'item': ticket}
    return render(request, 'reviews/delete_ticket.html', context)


@login_required(login_url='login')
def createReview(request, pk):
    form = ReviewForm(initial={'ticket': pk})    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request, 'reviews/review_form.html', context)


@login_required(login_url='login')
def updateReview(request, pk):
    review = Review.objects.get(pk=pk)
    form = ReviewForm(instance=review)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request, 'reviews/review_form.html', context)


def deleteReview(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('/')
    context = {'item': review}
    return render(request, 'reviews/delete_review.html', context)