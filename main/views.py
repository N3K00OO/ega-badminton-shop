from django.shortcuts import render

def home(request):
    ctx = {
        "my_app_name": "Toko Bola Ega",
        "my_name": "Gregorius Ega Aditama Sudjali",
        "pbp_class": "PBP C",
    }
    return render(request, "main/home.html", ctx)
