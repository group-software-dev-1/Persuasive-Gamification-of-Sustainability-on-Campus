from django.shortcuts import render


def index(request):
    return render(request, '../home/index.html', {"is_staff": request.user.is_staff})

def howto(request):
    return render(request, '../home/howto.html', {"is_staff": request.user.is_staff})

def goals(request):
    return render(request, '../home/goals.html', {"is_staff": request.user.is_staff})

def privacy(request):
    return render(request, '../home/privacy.html', {"is_staff": request.user.is_staff})