import sqlite3
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from learning_django import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
User = get_user_model()


# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address = request.POST['address']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.address = address
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        myuser.is_active = True
        return redirect('/')    
    return render(request, "authentication/signup.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def users(request):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    a = list(cur.execute ("SELECT * FROM 'authentication_customuser' "))
    lists = []
    for i in range(1, len(a)):
        e = {}
        e["username"] = (a[i][4])
        e["email"] = (a[i][7])
        e["address"] = (a[i][11])
        e["id"  ] = (a[i][0])
        lists.append(e)
    return render(request, 'authentication/users.html',{"lists" : lists})


def delete(request, id):
    # print(id)
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute ("Delete FROM 'authentication_customuser' where id = {} ". format(id))
    conn.commit()
    return redirect('/users')

def update(request, id):
    print(1)
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    a = list(cur.execute ("Select * from 'authentication_customuser' where id = {} ". format(id)))
    username = ""
    email = ""
    address = ""
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
    
    if username == "" :
        username = a[0][4]
    
    if email == "" :
        email = a[0][7]
    
    if address == "" :
        address = a[0][11]
    
    print(email)
    e = "UPDATE 'authentication_customuser' SET username = \" {} \", email = \"{} \", address = \"{} \"   where id = {} ". format(str(username), str(email), str(address), id)
    print(e)
    cur.execute (e)
    conn.commit()
    return redirect('/users')
    