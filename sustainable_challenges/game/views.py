from django.shortcuts import render

def game(request):
    """
    This function renders the game page
    """
    # The user, game manager and current level is retrieved 
    user = request.user 
    game_manager = user.get_game_manager()
    current_level = game_manager.get_current_level()

    # A context is made for the current level
    current_context = {'name':current_level.get_name(), 'tasks':current_level.get_tasks(), 'points':current_level.get_points(), 'number':current_level.get_number()}

    # A for loop generated context for next 9 levels
    level_contexts = []
    for i in range(1,10):
        # The level number tasks needed, points and name are set
        level_num = current_level.get_number() + i
        tasks = 1
        points = 100
        name = 'litter'

        # Every 5th level has five tasks for 1000 pts
        if level_num % 5 == 0:
            points = 1000
            tasks = 5
        
        # Every 2nd lvl is a energy saving level and every 3rd level is a poi level
        if level_num % 2 == 0:
            name = 'saving'
        elif level_num % 3 == 0:
            name = 'interest'

        # The context ofr level is made and appended to the list
        context = {'name':name, 'tasks':tasks, 'points':points, 'number':level_num}
        level_contexts.append(context)

    # A list of level context is created and then give as an argument when rendering the page
    context = {"current_context": current_context, 'level_contexts':level_contexts, 'is_staff': user.is_staff,}
    return render(request, "game/game.html", context)

def shop(request):
    """
    This function renders the shop page
    """
    # Initial values for response and success are set
    response = False
    success = False

    # A dictionary converts prizes to points
    prize_to_points = {'amazon': 10000, 'john_lewis':10000, 'blackwells':50000, 'ram':50000, 'student_guild':50000, 'marketplace':50000}

    # A check is made to see if it is a post request e.g. user trying to redeem points
    if request.method == 'POST':
        # Response is set to true 
        response = True

        # The prize and required points is retrieved
        prize = request.POST['prize']
        required_points = prize_to_points[prize]

        if request.user.points >= required_points:
            # If the user has enough points success is true and points are removed
            success = True
            request.user.points -= required_points
            request.user.save()

    # A dictionary is made for how complete each prize is 
    completion = {}
    for k,v in prize_to_points.items():
        completion[k] = request.user.points * 100 / v

    # The page is rendered with context for the prizes 
    return render(request, "game/shop.html", {'completion':completion, 'prize_to_points':prize_to_points, 'points': request.user.points, 'success':success, 'response': response, 'is_staff': request.user.is_staff})