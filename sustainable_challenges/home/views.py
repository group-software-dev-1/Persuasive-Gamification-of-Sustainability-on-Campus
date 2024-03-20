from django.shortcuts import render


def index(request):
    return render(request, '../home/index.html', {"is_staff": request.user.is_staff})