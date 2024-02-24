from django.shortcuts import render

def game(request):
    context = {"level_numbers": list(range(1,11))}
    return render(request, "game/game.html", context)

def shop(request):
    return render(request, "game/shop.html")