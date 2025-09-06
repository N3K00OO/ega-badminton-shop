from django.shortcuts import render

def home(request):
    ctx = {
        "app_name": "main",
        "student_name": "Gregorius Ega Aditama Sudjali",
        "class_name": "Kelas kamu",
    }
    return render(request, "main/home.html", ctx)
