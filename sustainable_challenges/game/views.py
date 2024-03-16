from django.shortcuts import render

def game(request):
    """
    This function renders the game page
    """
    # A list of how many levels is created and then give as an argument when rendering the page
    context = {"level_numbers": list(range(1,11)), 'is_staff': request.user.is_staff}
    return render(request, "game/game.html", context)

def shop(request):
    """
    This function renders the shop page
    """
    return render(request, "game/shop.html", {'is_staff': request.user.is_staff})