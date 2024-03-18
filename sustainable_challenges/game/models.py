from django.db import models

# Create your models here.
class GameManager:
   
    def __init__(self) -> None:
        self._current_level = LitterLevel(1, 100, 1)

    def bind_user(self, user):
        self.user = user

    def get_current_level(self):
        return self._current_level
    
    def complete_task(self, task_name):
        if task_name == self.current_level.get_name():
            self.current_level.complete_task()

            if self.current_level.get_tasks() == 0:
                self._user.points += self.current_level.get_points()

                next_num = self.current_level.get_number() + 1
                next_points = 100
                num_tasks = 1

                if next_num % 5 == 0:
                    next_points = 1000
                    num_tasks = 5
                
                if next_num % 2 == 0:
                    self.current_level = SavingLevel(next_num, next_points, num_tasks)
                elif next_num % 3 == 0:
                    self.current_level = InterestLevel(next_num, next_points, num_tasks)
                else:
                    self.current_level = LitterLevel(next_num, next_points, num_tasks)

            return True
        else:
            return False

class Level:
    
    def __init__(self, number, points, tasks) -> None:
        self._points = points
        self._number = number
        self._tasks = tasks

    def complete_task(self):
        tasks -= 1

    def get_name(self):
        return self._name
    
    def get_tasks(self):
        return self._tasks
    
    def get_points(self):
        return self._points
    
    def get_number(self):
        return self._number


class LitterLevel(Level):
    _name = "litter"

class SavingLevel(Level):
    _name = "saving"

class InterestLevel(Level):
    _name = "interest"