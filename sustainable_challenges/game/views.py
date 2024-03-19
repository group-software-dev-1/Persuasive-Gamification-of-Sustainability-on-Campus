from django.shortcuts import render

def game(request):
    """
    This function renders the game page
    """
    user = request.user  # Retrieve the current logged-in user
    game_manager = user.get_game_manager()
    user.complete_task('litter')
    current_level = game_manager.get_current_level()
    current_context = {'name':current_level.get_name(), 'tasks':current_level.get_tasks(), 'points':current_level.get_points(), 'number':current_level.get_number()}

    level_contexts = []
    for i in range(1,10):
        level_num = current_level.get_number() + i
        tasks = 1
        points = 100
        name = 'litter'
        if level_num % 5 == 0:
            points = 1000
            tasks = 5
        
        if level_num % 2 == 0:
            name = 'saving'
        elif level_num % 3 == 0:
            name = 'interest'

        context = {'name':name, 'tasks':tasks, 'points':points, 'number':level_num}
        level_contexts.append(context)

    # A list of how many levels is created and then give as an argument when rendering the page
    context = {"current_context": current_context, 'level_contexts':level_contexts, 'is_staff': user.is_staff,}
    return render(request, "game/game.html", context)

def shop(request):
    """
    This function renders the shop page
    """
    return render(request, "game/shop.html", {'is_staff': request.user.is_staff})