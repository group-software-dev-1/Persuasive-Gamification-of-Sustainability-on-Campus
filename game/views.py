from django.shortcuts import redirect, render
from django.core.mail import send_mail

from .models import Raffle

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
            # Send user an email with there prize
            subject = "Congrats You Won!"
            message = "Well done on getting {} points and redeeming your prize. \n Here is the code to redeem your prize: ABCD-1EF2GH-IJ123".format(required_points)
            send_mail(subject, message, 'Group.Software.Dev.Help@gmail.com', [request.user.email])

    # A dictionary is made for how complete each prize is 
    completion = {}
    for k,v in prize_to_points.items():
        completion[k] = request.user.points * 100 / v

    # The page is rendered with context for the prizes 
    return render(request, "game/shop.html", {'completion':completion, 'prize_to_points':prize_to_points, 'points': request.user.points, 'success':success, 'response': response, 'is_staff': request.user.is_staff})

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
