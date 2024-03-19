from django.db import models

# Create your models here.
class GameManager:
   
    def __init__(self, points, level, tasks_till_next) -> None:
        self._points = points
        if level % 2 == 0:
            self._current_level = SavingLevel(level, tasks_till_next)
        elif level % 3 == 0:
            self._current_level = InterestLevel(level, tasks_till_next)
        else:
            self._current_level = LitterLevel(level, tasks_till_next)

    def get_current_level(self):
        return self._current_level
    
    def complete_task(self, task_name):
        if task_name == self._current_level.get_name():
            self._current_level.complete_task()

            if self._current_level.get_tasks() == 0:
                self._points += self._current_level.get_points()

                next_num = self._current_level.get_number() + 1
                num_tasks = 1

                if next_num % 5 == 0:
                    num_tasks = 5
                
                if next_num % 2 == 0:
                    self._current_level = SavingLevel(next_num, num_tasks)
                elif next_num % 3 == 0:
                    self._current_level = InterestLevel(next_num, num_tasks)
                else:
                    self._current_level = LitterLevel(next_num, num_tasks)

            return self._current_level.get_number(), self._points, self._current_level.get_tasks()
        else:
            return self._current_level.get_number(), self._points, self._current_level.get_tasks()

class Level:
    
    def __init__(self, number, tasks) -> None:
        self._number = number
        self._tasks = tasks
        if number % 5 == 0:
            self._points = 1000
        else:
            self._points = 100

    def complete_task(self):
        self._tasks -= 1

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