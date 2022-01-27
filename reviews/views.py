from email import message
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from crispy_forms.layout import Submit

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

def get_users_viewable_reviews(user):
    subscriptions = UserFollows.objects.filter(user=user)
    ticket_query = Ticket.objects.filter(user=user)
    query = Review.objects.filter(user=user)
        
    
    for s in subscriptions:
        query = query | Review.objects.filter(user=s.followed_user)
    for t in ticket_query:
        query = query | Review.objects.filter(ticket=t)
    return query


def get_users_viewable_tickets(user):
    subscriptions = UserFollows.objects.filter(user=user)
    query = Ticket.objects.filter(user=user)
    for s in subscriptions:
        query = query | Ticket.objects.filter(user=s.followed_user)        
    return query



@login_required(login_url='login')
def dashboard(request):    
    #reviews = Review.objects.all()
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    #tickets = Ticket.objects.all() 
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    final_tickets = []

    for t in tickets:
        if not Review.objects.filter(ticket=t).exists():
            final_tickets.append(t)
    
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, final_tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    
    return render(request, 'reviews/dashboard.html',  context={'posts': posts})


@login_required(login_url='login')
def posts(request):    
    reviews = Review.objects.filter(user=request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    #tickets = Ticket.objects.all() 
    tickets = Ticket.objects.filter(user=request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    return render(request, 'reviews/posts.html',  context={'posts': posts})

@login_required(login_url='login')
def subscriptions(request):
    user = request.user
    followed_users = UserFollows.objects.filter(user=user)
    following_users = UserFollows.objects.filter(followed_user=user)
    context = {'followed_users': followed_users, 'following_users': following_users}
    return render(request, 'reviews/subscriptions.html', context)


@login_required(login_url='login')
def createTicket(request):
    form = TicketForm()    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket = TicketForm(request.POST, request.FILES, instance=ticket)
            ticket.save()
            return redirect('/')
    
    if not form.helper.inputs:
        form.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
    context = {"form":form}
    return render(request, 'reviews/ticket_form.html', context)


@login_required(login_url='login')
def updateTicket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    form = TicketForm(instance=ticket)   
    if not form.helper.inputs:
        form.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('/')
        if not form.helper.inputs:
            form.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
    
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
    ticket = Ticket.objects.get(id=pk)  
    if not form.helper.inputs:
        form.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        form.instance.ticket = ticket
        form.instance.user = request.user

        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form, 'ticket':ticket}
    return render(request, 'reviews/review_form.html', context)


@login_required(login_url='login')
def updateReview(request, pk):
    review = Review.objects.get(pk=pk)
    ticket = review.ticket
    form = ReviewForm(instance=review)
    
    if request.user != review.user:
        return redirect('/')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/')
    if not form.helper.inputs:
        form.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
        
    context = {"form":form, 'ticket':ticket}
    return render(request, 'reviews/review_form.html', context)


@login_required(login_url='login')
def deleteReview(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('/')
    context = {'item': review}
    return render(request, 'reviews/delete_review.html', context)


@login_required(login_url='login')
def createTicketReview(request):
    form_ticket = TicketForm()
    form_review = ReviewForm()
    
    form_ticket.helper.inputs = []
    form_review.helper.inputs = []
    
    form_ticket.helper.form_tag = False
    form_review.helper.form_tag = False
    if request.method == 'POST':
        try:
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            form_ticket = TicketForm(request.POST, request.FILES, instance=ticket)
            if form_ticket.is_valid():
                ticket_id = form_ticket.save()
            
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket_id
            review.rating = request.POST.get('rating')
            form_review = ReviewForm(request.POST, instance=review)
            
            if form_review.is_valid():
                form_review.save()
            else:
                ticket_id.delete()
        except Exception as e:
            return redirect('create_review')
        return redirect('dashboard')
    if not form_review.helper.inputs:
        form_review.helper.add_input(Submit('submit', 'Valider', css_class='btn-primary float-right'))
    context = {'form_ticket': form_ticket, 'form_review': form_review}
    return render(request, 'reviews/create_ticket_review.html', context)

def subscribe(request):
    if request.method == 'POST':
        followed_user_username = request.POST.get('follow_user')
        user = request.user
        try:
            followed_user = User.objects.get(username=followed_user_username)
            follow_instance = UserFollows.objects.create(user=user, followed_user=followed_user)
            form = UserFollowsForm(instance=follow_instance)
            if form.is_valid():
                form.save()
        except:
            # TODO message 
            return redirect('subscriptions')
    return redirect('subscriptions')

def unsubscribe(request, pk):
    if request.method == 'POST':
        user = request.user
        follow_instance = UserFollows.objects.get(id=pk)
        if follow_instance.user == user:
            follow_instance.delete()
        return redirect('subscriptions')
