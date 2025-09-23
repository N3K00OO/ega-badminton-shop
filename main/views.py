import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.forms.forms import ProductForm
from django.contrib import messages

from main.models import Product

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()

    student = {
        "title": "Football News",
        "npm": "2406434153",
        "name": "Gregorius Ega Aditama Sudjali",
        "kelas": "PBP C",
        "username": request.user.username,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }
    return render(request, "main/main.html", {"products": products, "student": student})

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)   
        product.user = request.user        
        product.save()  
        return redirect("main:show_main")
    return render(request, "main/create_product.html", {"form": form})


@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()
    return render(request, "main/product_detail.html", {"product": product})


def show_xml(request):
    data = Product.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    data = Product.objects.all()
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")



def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    if not data.exists():
        return HttpResponse(status=404)
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json_by_id(request, id):
    try:
        obj = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    json_data = serializers.serialize("json", [obj]) 
    return HttpResponse(json_data, content_type="application/json")


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'main/register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'main/login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

 



