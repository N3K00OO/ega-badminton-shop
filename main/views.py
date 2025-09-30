import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.core import serializers

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.forms.forms import ProductForm
from django.contrib import messages

from main.models import Product

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import Product



@login_required(login_url='/login')
def show_main(request):
    filter_type   = request.GET.get("filter", "all")
    category_code = request.GET.get("category", "all")

    qs = Product.objects.select_related("user")

    if filter_type == "my":
        qs = qs.filter(user=request.user)

    if category_code != "all":
        code_to_label = dict(Product.categories())
        codes   = list(code_to_label.keys())
        labels  = list(code_to_label.values())
        label   = code_to_label.get(category_code)

        query = Q(category=category_code)
        if label:
            query |= Q(category__iexact=label) 
        if category_code == "misc":
            query |= (~Q(category__in=codes + labels)
                      & ~Q(category__isnull=True)
                      & ~Q(category=""))

        qs = qs.filter(query)

    products = qs.order_by("-created_at")

    student = {
        "title": "Football News",
        "npm": "2406434153",
        "name": "Gregorius Ega Aditama Sudjali",
        "kelas": "PBP C",
        "username": request.user.username,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }

    context = {
        "products": products,
        "student": student,
        "last_login": student["last_login"],
        "current_filter": filter_type,
        "current_category": category_code,
        "categories": Product.categories(),
        "is_all_active": filter_type != "my",
        "is_my_active":  filter_type == "my",
    }
    return render(request, "main/main.html", context)


@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user

        category_code = form.cleaned_data.get("category")
        custom = form.cleaned_data.get("category_custom", "").strip()
        if category_code == "misc" and custom:
            product.category = custom 

        product.save()
        return redirect("main:show_main")
    return render(request, "main/create_product.html", {"form": form, "categories": Product.categories()})


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


@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return HttpResponseForbidden("You cannot edit this product.")

    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated.")
        return redirect("main:show_product", id=str(product.pk))

    return render(request, "main/edit_product.html", {"form": form, "product": product})



@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return HttpResponseForbidden("You cannot delete this product.")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("main:show_main")

    return render(request, "main/confirm_delete.html", {"product": product})

 



