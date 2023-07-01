from django.shortcuts import render, redirect
from bootstrap import models as bootstrap_models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from . import models
# Create your views here.


def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path == '/myadmin/' or request.path == "/myadmin/managecustomer/" or request.path == "/myadmin/addcategory/" or request.path == "/myadmin/subcategory/":
            if request.session['semail'] == None or request.session['srole'] != "admin":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def adminhome(request):
    return render(request, "adminhome.html", {"semail": request.session["semail"]})


def managecustomer(request):
    customer = bootstrap_models.Register.objects.filter(role='user')
    return render(request, "managecustomer.html", {"customer": customer, "semail": request.session["semail"]})


def customerstatus(request):
    regid = request.GET.get("regid")
    S = request.GET.get("S")
    print(S)

    if S == "block":
        bootstrap_models.Register.objects.filter(
            regid=int(regid)).update(status=0)
        return redirect("/myadmin/managecustomer/")

    elif S == "Verify":
        bootstrap_models.Register.objects.filter(
            regid=int(regid)).update(status=1)
        return redirect("/myadmin/managecustomer/")

    else:
        bootstrap_models.Register.objects.filter(regid=int(regid)).delete()
        return redirect("/myadmin/managecustomer/")


def addcategory(request):
    if request.method == "GET":
        return render(request, "addcategory.html", {"semail": request.session["semail"]})
    else:
        catnm = request.POST.get("catnm")
        caticon = request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name, caticon)
        print(catnm)
        n = models.Category(catnm=catnm, caticonname=filename)
        n.save()
        return render(request, "addcategory.html", {"output": "Category Added Successfully", "semail": request.session["semail"]})


def subcategory(request):
    list = models.Category.objects.all()
    if request.method == "GET":
        return render(request, "subcategory.html", {"list": list, "semail": request.session["semail"]})
    else:
        catnm = request.POST.get("catnm")
        price = request.POST.get("price")
        description = request.POST.get("description")
        sprice = request.POST.get("sprice")
        subcatnm = request.POST.get("subcatnm")
        subcaticon = request.FILES['subcaticon']
        fs = FileSystemStorage()
        filename = fs.save(subcaticon.name, subcaticon)
        r = models.Subcategory(catnm=catnm, subcatnm=subcatnm,
                               subcaticon=filename, sprice=sprice, description=description)
        r.save()
        return render(request, "subcategory.html", {"list": list, "output": "Sub-category Added Successfully", "semail": request.session["semail"]})


def changpass(request):
    if request.method == "GET":
        return render(request, "changpass.html", {"semail": request.session["semail"]})
    else:
        oldpass = request.POST.get("oldpass")
        newpass = request.POST.get("newpass")
        conformpass = request.POST.get("conformpass")
        z = bootstrap_models.Register.objects.filter(email=request.session["semail"], password=oldpass).exists()
        if z:
            if newpass == conformpass:
                bootstrap_models.Register.objects.filter(email=request.session["semail"], password=oldpass).update(password=conformpass)
                return render(request, "changpass.html", {"output": "Password Change Successfully", "semail": request.session["semail"]})
            else:
                return render(request, "changpass.html", {"output": "new and conform password mismatch"})
        else:
            return render(request, "changpass.html", {"output": "Invalid old password"})
