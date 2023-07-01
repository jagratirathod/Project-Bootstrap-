
from django.conf import settings
from . import sendEmail
from myadmin import models as myadmin_models
import time
from django.shortcuts import redirect, render
from django.db import models
media_url = settings.MEDIA_URL
from . import models

def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path == '' or request.path == '/signup/' or request.path == '/login/':
            request.session['semail'] = None
            request.session['srole'] = None
            response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def home(request):
    list = myadmin_models.Category.objects.all()
    return render(request, "home.html", {"list": list, "media_url": media_url})


def viewsubcategory(request):
    catnm = request.GET.get("catnm")
    list = myadmin_models.Category.objects.all()
    slist = myadmin_models.Subcategory.objects.filter(catnm=catnm)
    subcatlist = myadmin_models.Subcategory.objects.all()
    return render(request, "viewsubcategory.html", {"catnm": catnm, "list": list, "slist": slist, "media_url": media_url, 'subcatlist': subcatlist})


def signup(request):
    if request.method == 'GET':
        return render(request, "signup.html")
    else:
        firstnm = request.POST.get("firstnm")
        lastnm = request.POST.get("lastnm")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        info = time.asctime()
        # sendEmail.mymail(email, password)
        p= models.Register(firstnm=firstnm, lastnm=lastnm, email=email, 
                            password=password, mobile=mobile, info=info, role="user", status=0)
        p.save()
        return render(request, "signup.html", {"output": "You Sign Up Successfully"})


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        Details = models.Register.objects.filter(email=email, password=password, status=1)
        if len(Details) > 0:
            request.session["semail"] = Details[0].email
            request.session["srole"] = Details[0].role

            if Details[0].role == "admin":
                return redirect("/myadmin/")
            else:
                return redirect("/user/")
        else:
            return render(request, "login.html", {'output': "Invalid user"})


def productfilter(request):
    sprice = request.GET.get("sprice")
    description = request.GET.get("description")
    subcatnm = request.GET.get("subcatnm")
    startprice = request.GET.get("startprice")
    endprice = request.GET.get("endprice")
    if startprice == None:
        vlist = myadmin_models.Subcategory.objects.filter(
            subcatnm=subcatnm, sprice=sprice, description=description)
    else:
        vlist = myadmin_models.Subcategory.objects.filter(
            subcatnm=subcatnm, sprice__range=(int(startprice), int(endprice)))
        print(vlist)

    sublist = myadmin_models.Subcategory.objects.all()
    return render(request, "productfilter.html", {'sublist': sublist, "media_url": media_url, 'subcatnm': subcatnm, "vlist": vlist, "sprice": sprice, ' description': description})

def verifyuser(request):
    email = request.GET.get("email")
    models.Register.objects.filter(email=email).update(status=1)
    return redirect("/login/")
