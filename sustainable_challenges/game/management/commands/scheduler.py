from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from game.models import Raffle
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from forum.models import Annoucement
from authuser.models import User

class Command(BaseCommand):
    help = 'Runs the raffle reset scheduler'

    def handle(self, *args, **kwargs):
        #creates a scheduler
        scheduler = BackgroundScheduler()
        #adds the daily and weekly raffle s to it, every 3pm and for weekly every friday 3pm
        scheduler.add_job(self.daily_raffle, 'cron', hour=15, minute=0, second=0)
        scheduler.add_job(self.weekly_raffle, 'cron', day_of_week='fri', hour=15, minute=0, second=0)
        print("We gaming")
        
        #starts the scheduler
        scheduler.start()

        #insures its running
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()


    


    #the daily raffle
    def daily_raffle(self):
        #gest the raffle with the matching name of Daily
        daily_raffle = Raffle.objects.filter(name='Daily').first()
        if daily_raffle:
            #if it has participants
            if daily_raffle.participants:
                #splits them up from the comma string to a list then picks a random winner
                daily_participants = daily_raffle.participants.split(',')
                daily_winner = random.choice(daily_participants)
                try:
                    #gest the winner with the macthing username
                    winner_user = User.objects.get(username=daily_winner)
                except User.DoesNotExist:
                    #if they dont exist
                    self.stdout.write(self.style.ERROR("Winner user not found."))
                self.stdout.write(self.style.SUCCESS(f"Daily Raffle Winner: {daily_winner}"))
                #If the winner is found as a match
                if winner_user:
                    #gives them the points
                    winner_user.points += daily_raffle.points_accumulated
                    winner_user.save()
                    annoucement = Annoucement.objects.create(
                        post_name='Daily Raffle Winner Annoucement',
                        post_text=f"Congratulations to {daily_winner} for winning the daily raffle!",
                        poster=winner_user
                    )

                    

                daily_raffle.save()
            else:
                self.stdout.write("No participants in the daily raffle.")
        else:
            self.stdout.write("Daily raffle not found.")
            #resets the raffle to starting point
        daily_raffle.points_accumulated = 200
        daily_raffle.participants = ''
        daily_raffle.num_participants = 0
        daily_raffle.save()

    #exact same just for the weekly one
    def weekly_raffle(self):


        weekly_raffle = Raffle.objects.filter(name='Weekly').first()
        if weekly_raffle:
            self.stdout.write("Weekly raffle found.")
            if weekly_raffle.participants:
                weekly_participants = weekly_raffle.participants.split(',')
                weekly_winner = random.choice(weekly_participants)
                try:
                    winner_user = User.objects.get(username=weekly_winner)
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR("Winner user not found."))
                self.stdout.write(self.style.SUCCESS(f"Weekly Raffle Winner: {weekly_winner}"))

                if winner_user:
                    winner_user.points += weekly_raffle.points_accumulated
                    winner_user.save()
                    annoucement = Annoucement.objects.create(
                        post_name='Daily Raffle Winner Annoucement',
                        post_text=f"Congratulations to {weekly_winner} for winning the daily raffle!",
                        poster=winner_user
                    )
                    self.stdout.write(self.style.SUCCESS(f"Points added to winner ({weekly_winner}): {weekly_raffle.points_accumulated}"))

                weekly_raffle.save()
            else:
                self.stdout.write("No participants in the weekly raffle.")
        else:
            self.stdout.write("Weekly raffle not found.")
        weekly_raffle.points_accumulated = 1000
        weekly_raffle.participants = ''
        weekly_raffle.num_participants = 0
        weekly_raffle.save()
