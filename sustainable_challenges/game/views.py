from django.shortcuts import render

def game(request):
    context = {"level_numbers": list(range(1,11)), 'is_staff': request.user.is_staff}
    return render(request, "game/game.html", context)

def shop(request):
    return render(request, "game/shop.html", {'is_staff': request.user.is_staff})