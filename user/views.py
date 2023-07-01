from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from bootstrap import models as bootstrap_models
from myadmin import models as myadmin_models
from . import models

import time
from django.db.models import Q
from django.conf import settings
media_url = settings.MEDIA_URL


def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path == '/user/' or request.path == "/user/changepassworduser/":
            if request.session['semail'] == None or request.session['srole'] != "user":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def userhome(request):
    return render(request, "userhome.html", {"semail": request.session["semail"]})


def changepassworduser(request):
    if request.method == "GET":
        return render(request, "changepassworduser.html", {"semail": request.session["semail"]})
    else:
        oldpass = request.POST.get("oldpass")
        newpass = request.POST.get("newpass")
        conformpass = request.POST.get("conformpass")
        z = bootstrap_models.Register.objects.filter(
            email=request.session["semail"], password=oldpass).exists()
        if z:
            if newpass == conformpass:
                bootstrap_models.Register.objects.filter(
                    email=request.session["semail"], password=oldpass).update(password=conformpass)
                return render(request, "changepassworduser.html", {"output": "Password Change Successfully", "semail": request.session["semail"]})
            else:
                return render(request, "changepassworduser.html", {"output": "new and conform password mismatch", "semail": request.session["semail"]})
        else:
            return render(request, "changepassworduser.html", {"output": "Invalid old password", "semail": request.session["semail"]})


def addproduct(request):
    lst = myadmin_models.Category.objects.all()
    if request.method == "GET":
        return render(request, "addproduct.html", {"semail": request.session["semail"], "lst":  lst})
    else:
        title = request.POST.get("title")
        category = request.POST.get("category")
        subcategory = request.POST.get("subcategory")
        description = request.POST.get("description")
        price = request.POST.get("price")
        file1 = request.FILES['file1']
        fs = FileSystemStorage()
        file1name = fs.save(file1.name, file1)
        info = time.time()
        p = models.Product(title=title, category=category, subcategory=subcategory, description=description,
                           price=price, file1=file1name, status=0, uid=request.session['semail'], info=info)
        p.save()
        return render(request, "addproduct.html", {"semail": request.session["semail"], "lst":  lst})


def fetchSubcategoryAJAX(request):
    catnm = request.GET.get("catnm")
    sclist = myadmin_models.Subcategory.objects.filter(catnm=catnm)
    print(catnm)
    sclist_options = "<option>select sub category</option>"
    for row in sclist:
        sclist_options += ("<option>"+row. subcatnm+"</option>")
    return HttpResponse(sclist_options)


def viewproduct(request):
    paypalURL = "http://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID = "sb-hky0g5755137@business.example.com"
    list = models.Product.objects.filter(uid=request.session["semail"])
    return render(request, "viewproduct.html", {"list": list, "semail": request.session["semail"], "paypalURL": paypalURL, "paypalID": paypalID})


def cancel(request):
    return render(request, "cancel.html", {"semail": request.session["semail"]})


def success(request):
    return render(request, "success.html", {"semail": request.session["semail"]})


def payment(request):
    pid = request.GET.get("pid")
    uid = request.GET.get("uid")
    amount = request.GET.get("amount")
    info = time.time()
    p = models.Payment(pid=int(pid), uid=uid, amount=amount, info=info)
    p.save()

    models.Product.objects.filter(pid=int(pid)).update(status=1, info=info)
    return redirect("/user/success/")


def bidproduct(request):
    plist = models.Product.objects.filter(~Q(uid=request.session["semail"]))
    pid = plist[0].pid
    print(pid)
    return render(request, "bidproduct.html", {"semail": request.session["semail"], "plist": plist, "pid": pid, "media_url": media_url})


def bidproductview(request):
    pid = int(request.GET.get("pid"))
    print(pid)
    price = int(request.GET.get("price"))
    bidlist = models.Bidding.objects.filter(pid=pid)
    if len(bidlist) > 0:
        bidDetails = models.Bidding.objects.filter(pid=pid)
        cprice = bidDetails[len(bidDetails)-1].bidamount
    else:
        cprice = price

    pDetails = models.Product.objects.filter(pid=pid)
    print(pDetails[0].info)
    if(time.time()-float(pDetails[0].info)) > 172800:
        bstatus = False
    else:
        bstatus = True
    return render(request, "bidproductview.html", {"semail": request.session["semail"], "pid": pid, "price": price, "cprice": cprice, "bstatus": bstatus})


def bidhistory(request):
    pid = request.GET.get("pid")
    bidlist = models.Bidding.objects.filter(pid=pid)
    return render(request, "bidhistory.html", {"semail": request.session["semail"], "pid": pid})


def mybid(request):
    pid = request.POST.get("pid")
    price= request.POST.get("price")
    cprice = request.POST.get("cprice")
    bidprice = request.POST.get("bidprice")
    p = models.Bidding(pid=pid, uid=request.session["semail"], bidamount=bidprice, info=time.asctime())
    p.save()
    return redirect("/user/bidproductview/?pid="+str(pid)+"&price="+str(price))
