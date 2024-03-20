from django.db import models

# Create your models here.
class GameManager:
    """
    Game manger manages the logic for the game for a user

    Fields
    ------
    _points : int
        The points the user is on
    _current_level: Level
        The level the user is currently on

    """
    def __init__(self, points, level, tasks_till_next) -> None:
        """
        Constructs game manger instance for user

        Parameters
        ----------
        points : int
            The point the user is on
        level : int
            The number of the level the user is on
        tasks_till_next : int
            The number of tasks till the next level
        """

        # The points field is set
        self._points = points

        # The level is the created on the logic
        # Every 2nd level is energy saving level
        # Every 3rd level is a poi level
        # Every other level is a litter level
        if level % 2 == 0:
            self._current_level = SavingLevel(level, tasks_till_next)
        elif level % 3 == 0:
            self._current_level = InterestLevel(level, tasks_till_next)
        else:
            self._current_level = LitterLevel(level, tasks_till_next)

    def get_current_level(self):
        """
        Getter for the current level

        Returns
        -------
        Level : the current level
        """
        return self._current_level
    
    def complete_task(self, task_name):
        """
        Runs the logic for completing a task

        Parameters
        ----------
        task_name : String
            The task that is being completed 

        Returns
        -------
        int : the number that the level is now on
        int : the points the user is now on
        int : the number of tasks the user has to complete for next level
        """

        # If statement checks if user has completed the required tasks
        if task_name == self._current_level.get_name():
            # A tasks for the level is completed
            self._current_level.complete_task()

            # If statement checks if all tasks for the level have been completed
            if self._current_level.get_tasks() == 0:
                # The points are added for completion, level number is increased and for now number of tasks is set to 1
                self._points += self._current_level.get_points()
                next_num = self._current_level.get_number() + 1
                num_tasks = 1

                # If the next level is a challenge level then the number of tasks is set to 5
                if next_num % 5 == 0:
                    num_tasks = 5
                
                # The level is the created on the logic
                # Every 2nd level is energy saving level
                # Every 3rd level is a poi level
                # Every other level is a litter level
                if next_num % 2 == 0:
                    self._current_level = SavingLevel(next_num, num_tasks)
                elif next_num % 3 == 0:
                    self._current_level = InterestLevel(next_num, num_tasks)
                else:
                    self._current_level = LitterLevel(next_num, num_tasks)

            # Finally the new level number, points and tasks needed are returned
            return self._current_level.get_number(), self._points, self._current_level.get_tasks()
        else:
            # If they haven't completed the required task they only gain 50 points
            return self._current_level.get_number(), self._points + 50, self._current_level.get_tasks()

class Level:
    """
    Level for the user to complete

    Fields
    ------
    _number : int
        number of the level
    _tasks : int
        tasks needed to complete the level
    _points : int
        points scored for completing the level
    """
    
    def __init__(self, number, tasks) -> None:
        """
        Constructs a new level instance
        
        Parameters
        ----------
        number : int
            The number of the level
        tasks : int
            The tasks needed to complete the level
        """
        # The number and tasks are set
        self._number = number
        self._tasks = tasks

        # The points are then set on the logic for if it is a challenge level
        if number % 5 == 0:
            self._points = 1000
        else:
            self._points = 100

    def complete_task(self):
        """
        Subtracts one from task counter
        """
        self._tasks -= 1

    def get_name(self):
        """
        Getter fo the levels name 

        Returns
        -------
        name : String 
            Levels name
        """
        return self._name
    
    def get_tasks(self):
        """
        Getter for number of tasks needed

        Returns
        -------
        tasks : int
            number of tasks needed
        """
        return self._tasks
    
    def get_points(self):
        """
        Getter for number of points

        Returns
        -------
        points : int
            number of points
        """
        return self._points
    
    def get_number(self):
        """
        Getter for level number 

        Returns
        -------
        number : int
            level number 
        """
        return self._number


class LitterLevel(Level):
    """
    Litter Level for the user to complete

    Fields
    ------
    _number : int
        number of the level
    _tasks : int
        tasks needed to complete the level
    _points : int
        points scored for completing the level
    _name : String
        The name of the level
    """
    _name = "litter"

class SavingLevel(Level):
    """
    Energy Saving Level for the user to complete

    Fields
    ------
    _number : int
        number of the level
    _tasks : int
        tasks needed to complete the level
    _points : int
        points scored for completing the level
    _name : String
        The name of the level
    """
    _name = "saving"

class InterestLevel(Level):
    """
    Point of Interest Level for the user to complete

    Fields
    ------
    _number : int
        number of the level
    _tasks : int
        tasks needed to complete the level
    _points : int
        points scored for completing the level
    _name : String
        The name of the level
    """
    _name = "interest"