from django.shortcuts import render,HttpResponse,redirect
from .models import *
import re 
from django.http import JsonResponse
import bcrypt

def index(request):
    return redirect('/show_login_form')
def showRegisterForm(request):
    return render(request,"register.html")
def validate_text(text, min_length=2):
    verified = True
    if not text:
        verified = False
    elif len(text) < min_length:
        verified = False
    return verified


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        if not is_duplicate_email(email):
            return True
    return False
def validate_name(name):
    NAME_REGEX=re.compile(r'^[a-zA-Z]+$')
    if not NAME_REGEX.match(name):
        return False
    return True


def register(request):
    errors={}
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # cnf_passwd = request.POST['confirm']
        if not validate_text(first_name):
            errors['first_name']="The name length shoud be graterthan two"
        if not validate_name(first_name):
            errors['first_name']="the name shold have only String"
        if not validate_text(last_name):
            errors['first_name']="The name length shoud be graterthan two"
        if not validate_name(last_name):
            errors['last_name']="the name shold have only String"
        if not validate_text(password, min_length=8):
            errors['pws']="should have at least 8 character"
        if not validate_email(email):
            errors['email']="the email not in correct format"
        if is_duplicate_email(email):
            errors['email']="the email already used"
        # if password!=cnf_passwd:
        #     errors['pws']="The password does not match"
        for key, value in errors.items():
            messages.error(request, value)
        if validate_text(first_name) and validate_text(last_name) and validate_text(password, min_length=8):
            # and validate_email(email) and password == cnf_passwd:
            passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = insert_new_user(first_name, last_name, email, passwd)
            if 'user_id' not in request.session:
                request.session['user_id'] = user.id
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                return redirect('/show_all_book')
    return redirect('/')

def login(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            return redirect('/show_all_book')
        else:
            email = request.POST['email']
            passwd = request.POST['password']
            # user = User.objects.filter(username=request.POST['username'])
            loggedUser=get_userByEmail(email)
            print(loggedUser)
            if loggedUser is not None:
                if bcrypt.checkpw(passwd.encode(),loggedUser.password.encode()):
                    if 'user_id' not in request.session:
                        request.session['user_id'] = loggedUser.id
                        request.session['first_name'] = loggedUser.first_name
                        request.session['last_name'] = loggedUser.last_name
                        return redirect('/show_all_book')
    return redirect('/show_register_form')

def showLoginForm(request):
    return render(request,"login.html")
def validateEmailByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the email is valid or not and return a json.
    the returnd json  carry a message if email is invalid
    the length of the message will be zero if the email valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['email']=''
        email=request.POST['email']
        if not validate_email(email):
            msg['email']="Email not valid"
            return JsonResponse(msg)
        if is_duplicate_email(email):
            msg['email']="sorry email in use ,choose another email"
        return JsonResponse(msg)
    return redirect('/')

def validateFirstNameByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the first name is valid or not and return a json.
    the returnd json  carry a message if first name is invalid
    the length of the message will be zero if the first name valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['fname']=''
        firstName=request.POST['fname']
        if not validate_text(firstName):
            msg['fname']="the name should be a text and greater the length grather than two "
            return JsonResponse(msg)
        if not validate_name(firstName):
            msg['fname']="The first name should be a text"
        return JsonResponse(msg)
    return redirect('/')

def validateLastNameByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the last name is valid or not and return a json.
    the returnd json  carry a message if last name is invalid
    the length of the message will be zero if the last name valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['lname']=''
        lastName=request.POST['lname']
        if not validate_text(lastName):
            msg['lname']=" the length should be  grather than two "
            return JsonResponse(msg)
            if not validate_name(lastName):
                msg['lname']="The first name should be a text"
        return JsonResponse(msg)
    return redirect('/')

def validatePasswordByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the password is valid or not and return a json.
    the returnd json  carry a message if password is invalid
    the length of the message will be zero if the password valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        password=request.POST['password']
        msg['password']=''
        if not validate_text(password, min_length=8):
            msg['password']="the length of password shoud be at least 8 charecter"
        return JsonResponse(msg)
    return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['first_name']
        del request.session['last_name']
    return redirect('/')


def showAllBook(request):
    allbook=Book.objects.all()
    id=request.session['user_id']
    # user=User.objects.get(id=id)
    context={
        "allbook":allbook,
        "id":id,
        "fname":request.session['first_name']
    }
    return render(request,"allbook.html",context)

def addBook(request):
    if "user_id" in request.session:
        userId=request.session['user_id']
        user=User.objects.get(id=userId)
        userWhoLike=User.objects.filter(id=userId)
        description=request.POST['description']
        title=request.POST['title']
        b=Book.objects.create(title=title,description=description,uploaded_By=user)
    return redirect("/show_all_book")
def show(request,id):
    bookId=int(id)
    userId=request.session['user_id']
    b=Book.objects.get(id=bookId)
    user=User.objects.get(id=userId)
    allliked=user.liked_book.all()
    flag=False
    for book in allliked:
        if book == b:
            flag=True
            break
    
    context={
        "book":b,
        "flag":flag
    }
    return render(request,"show.html",context)

def addFavorite(request,id):
    bookId=int(id)
    userId=request.session['user_id']
    book=Book.objects.get(id=bookId)
    user=User.objects.get(id=userId)
    user.liked_book.add(book)
    return redirect("/show_all_book")
def unfavorite(request,id):
    bookId=int(id)
    book=Book.objects.get(id=bookId)
    userId=request.session['user_id']
    user=User.objects.get(id=userId)
    user.liked_book.remove(book)
    return redirect("/show_all_book")
def editForm(request,id):
    bookId=int(id)
    b=Book.objects.get(id=bookId)
    userId=request.session['user_id']
    user=User.objects.get(id=userId)
    userWhoLike=b.user_who_like.all()
    allliked=user.liked_book.all()
    flag=False
    for book in allliked:
        if book == b:
            flag=True
            break
    context={
        "book":b,
        "userWhoLike":userWhoLike,
        "flag":flag
    }
    return render(request,"edit.html",context)





# Create your views here.
