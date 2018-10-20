from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from datetime import datetime, timezone
import time

def index(request):

    if 'login' not in request.session:
        request.session['login'] = False
        request.session['id'] = []
    else:
        request.session['id'] = []
    return render(request, "theWall/index.html")

temp = ""
def register(request):
    temp = request.POST['password']
    errors = User.objects.checkRegistration(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        pwHash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        temp = pwHash
        newUser = User.objects.create(first_name = request.POST['first_name'],
                                      last_name = request.POST['last_name'], 
                                      email = request.POST['email'], 
                                      password = pwHash.decode('utf-8'))
        request.session['login'] = True
        request.session['id'] = User.objects.get(email=request.POST['email']).id # what do u know i guess this worked
        return redirect('/success')

def success(request):
    if request.session['login'] == False:
        err = "Please log in"
        messages.error(request, err)
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
        'usermessages': Message.objects.order_by("-created_at")
    }
    return render(request, "theWall/success.html", context)

def login(request):

    errors = User.objects.checkLogin(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        request.session['login'] = True
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/success')

def message(request):
    Message.objects.create(content=request.POST['message'], 
                           user_id = User.objects.get(id=request.session['id']))
    return redirect('/success')

def comment(request):
    Comment.objects.create(content=request.POST['comment'],
                           user_id = User.objects.get(id=request.session['id']),
                           message_id = Message.objects.get(id=request.POST['message']))
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request):
    now = datetime.now(timezone.utc)
    message = Message.objects.get(id=request.POST['delete'])
    elapsed = now - message.created_at
    if (elapsed.seconds/60) > 30:
        errMsg = "Were sorry. We can not remove a comment after it's been up for 30 minutes"
        messages.error(request, errMsg)
        return redirect('/success')
    else:
        message.delete()
        return redirect('/success')