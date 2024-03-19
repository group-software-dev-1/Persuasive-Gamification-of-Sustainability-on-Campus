from django.shortcuts import redirect, render

from .models import Raffle

def game(request):
    """
    This function renders the game page
    """
    user = request.user  # Retrieve the current logged-in user
    game_manager = user.get_game_manager()
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

def raffle(request):
    #gets the raffles by checking their names
    daily_raffle = Raffle.objects.filter(name='Daily').first()
    weekly_raffle = Raffle.objects.filter(name='Weekly').first()
    #creates 2 empty lists for each one and then adds the usernames from the string, splitting them from the commas
    daily_participants = []  
    if daily_raffle.participants:
        daily_participants = daily_raffle.participants.split(',')

    weekly_participants = []  
    if weekly_raffle.participants:
        weekly_participants = weekly_raffle.participants.split(',')

    #gets the user
    user = request.user

    #If a post is recieved from the page checks does the following
    if request.method == 'POST':
        #cgets the attacthed code and username
        code = request.POST.get('code')
        username = request.POST.get('username')
        #if the code is daily
        if code == 'daily':
            #and the username isnt in the list already
            if username not in daily_participants:
                #if its the first entry
                if daily_participants == []:
                    #adds it immediately to the string
                    daily_raffle.participants += username
                else:
                    #otherwise puts a comma, and then the username
                    daily_raffle.participants += ',' + username 
                #increase the int for the particpants and then saves
                daily_raffle.num_participants += 1
                daily_raffle.save()

        elif code == 'weekly':
            #exactly the same for weekly
            if username not in weekly_participants:
                if user.points >= 100:  #but does a check to see if they have the points required to enter
                    if weekly_participants == []:
                        weekly_raffle.participants += username
                    else:
                        weekly_raffle.participants += ',' + username 
                    weekly_raffle.num_participants += 1
                    weekly_raffle.points_accumulated += 100
                    weekly_raffle.save()
                    # After adding takes away the points they entered with
                    user.points -= 100
                    user.save()
                else:
                    print("User does not have enough points to enter the Weekly Raffle.")
            else:
                print("User has already entered the Weekly Raffle.")
        return redirect('game:raffle')
    #basic context for the html
    context = {
        'daily_raffle': daily_raffle,
        'daily_participants': daily_participants,
        'weekly_raffle': weekly_raffle,
        'weekly_participants': weekly_participants,
        'is_staff': request.user.is_staff,
    }
    
    return render(request, "game/raffle.html", context)