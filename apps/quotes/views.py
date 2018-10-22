from django.shortcuts import render, redirect
from .models import User, Quote, Like
from django.contrib import messages
import bcrypt

def index(request):
    if 'login' not in request.session:
        request.session['login'] = False
    else: 
        request.session['login'] = False
        request.session['id'] = []
    return render(request, 'quotes/index.html')

def register(request):
    errors = User.objects.checkRegistration(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else: 
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'],
                            last_name = request.POST['last_name'],
                            email = request.POST['email'],
                            password = pw_hash.decode('utf-8'))
        request.session['login'] = True
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/success')

def login(request):
    errors = User.objects.checkLogin(request.POST)
    if len(errors):
        for key, value in errors.items():
            messagers.error(request, value)
            return redirect('/')
    else: 
        user = User.objects.get(email = request.POST['email'])
        request.session['login'] = True
        request.session['id'] = user.id
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'quotes': Quote.objects.all()
    }
    return render(request, 'quotes/success.html', context)

def editUser(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request,'quotes/edit.html', context)

def updateUser(request):
    errors = User.objects.checkUpdate(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    else:
        user = User.objects.get(id=request.session['id'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, "Info successfully updated")
    return redirect('/edituser')

def create(request):
    print("_"*50, request.session['id'])
    errors = Quote.objects.checkQuote(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    else:
        user = User.objects.get(id = request.POST['posted_by'])
        Quote.objects.create(author = request.POST['author'],
                            content = request.POST['quote'],
                            user = user)
    return redirect('/success')

def like(request):
    user = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=request.POST['liked_quote'])
    print(quote.likes.all())
    for like in quote.likes.all():
        if like.user.id == user.id:
            return redirect('/success')
    Like.objects.create(user = User.objects.get(id = request.session['id']),
                        quote = Quote.objects.get(id = request.POST['liked_quote']))
    return redirect('/success')

def delete(request):
    quote = Quote.objects.get(id=request.POST['delete_quote'])
    quote.delete()
    return redirect('/success')

def user(request, num):
    user = User.objects.get(id=num)
    quotes = user.quotes.all()
    context = {
        'user' : user,
        'quotes': quotes
    }
    return render(request, 'quotes/user.html', context)