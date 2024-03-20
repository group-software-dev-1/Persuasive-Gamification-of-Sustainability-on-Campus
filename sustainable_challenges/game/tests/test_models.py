from django.test import TestCase
from game.models import *

class TestGameManager(TestCase):
    """
    Test suite for the game manager
    """

    def test_get_current_level(self):
        """
        Tests getter fo the current level
        """
        manager = GameManager(100, 1, 1)
        expected_results = manager._current_level
        self.assertEqual(expected_results, manager.get_current_level())

    def test_complete_task_not_level(self):
        """
        Tests when completing a task that isn't required for current level
        """
        manager = GameManager(100, 1, 1)
        expected_results = (1, 150, 1)
        self.assertEqual(expected_results, manager.complete_task('saving'))

    def test_complete_task_required_not_level(self):
        """
        Test for when completing a required task but not the level
        """
        manager = GameManager(100, 1, 2)
        expected_results = (1, 100, 1)
        self.assertEqual(expected_results, manager.complete_task('litter'))

    def test_complete_task_complete_level(self):
        """
        Tests for when completing a task that completes the level
        """
        manager = GameManager(100, 1, 1)
        expected_results = (2, 200, 1)
        self.assertEqual(expected_results, manager.complete_task('litter'))

    def test_complete_task_challenge_level(self):
        """
        Test for when completing a challenge level worth 1000 points
        """
        manager = GameManager(100, 5, 1)
        expected_results = (6, 1100, 1)
        self.assertEqual(expected_results, manager.complete_task('litter'))
    
    def test_complete_task_onto_saving(self):
        """
        Tests when completing a level if the next level is a saving level when level number is multiple of 2
        """
        manager = GameManager(100, 1, 1)
        manager.complete_task('litter')
        self.assertTrue(isinstance(manager._current_level, SavingLevel))

    def test_complete_task_onto_interest(self):
        """
        Tests when completing a level if the next level is a interest level when level number is multiple of 3
        """
        manager = GameManager(100, 2, 1)
        manager.complete_task('saving')
        self.assertTrue(isinstance(manager._current_level, InterestLevel))

    def test_complete_task_onto_litter(self):
        """
        Tests when completing a level if the next level is a litter level when level number is not multiple of 2 or 3
        """
        manager = GameManager(100, 4, 1)
        manager.complete_task('saving')
        self.assertTrue(isinstance(manager._current_level, LitterLevel))


class TestLitterLevel(TestCase):
    
    def test_complete_task(self):
        """
        Tests for completing a task for the level
        """
        level = LitterLevel(5,5)
        level.complete_task()
        except_result = 4
        self.assertEqual(except_result, level._tasks)

    def test_get_name(self):
        """
        Tests getter for levels name
        """
        level = LitterLevel(1,1)
        self.assertEqual(level._name, level.get_name())

    def test_get_tasks(self):
        """
        Test getter for number of tasks
        """
        level = LitterLevel(1,1)
        self.assertEqual(level._tasks, level.get_tasks())

    def test_get_points(self):
        """
        Test getter for number of points the level is worth
        """
        level = LitterLevel(1,1)
        self.assertEqual(level._points, level.get_points())

    def test_get_number(self):
        """
        Test getter for the number of the level 
        """
        level = LitterLevel(1,1)
        self.assertEqual(level._number, level.get_number())

class TestSavingLevel(TestCase):


    def test_complete_task(self):
        """
        Tests for completing a task for the level
        """
        level = SavingLevel(5,5)
        level.complete_task()
        except_result = 4
        self.assertEqual(except_result, level._tasks)

    def test_get_name(self):
        """
        Tests getter for levels name
        """
        level = SavingLevel(1,1)
        self.assertEqual(level._name, level.get_name())

    def test_get_tasks(self):
        """
        Test getter for number of tasks
        """
        level = SavingLevel(1,1)
        self.assertEqual(level._tasks, level.get_tasks())

    def test_get_points(self):
        """
        Test getter for number of points the level is worth
        """
        level = SavingLevel(1,1)
        self.assertEqual(level._points, level.get_points())

    def test_get_number(self):
        """
        Test getter for the number of the level 
        """
        level = SavingLevel(1,1)
        self.assertEqual(level._number, level.get_number())

class TestInterestLevel(TestCase):

    def test_complete_task(self):
        """
        Tests for completing a task for the level
        """
        level = InterestLevel(5,5)
        level.complete_task()
        except_result = 4
        self.assertEqual(except_result, level._tasks)

    def test_get_name(self):
        """
        Tests getter for levels name
        """
        level = InterestLevel(1,1)
        self.assertEqual(level._name, level.get_name())

    def test_get_tasks(self):
        """
        Test getter for number of tasks
        """
        level = InterestLevel(1,1)
        self.assertEqual(level._tasks, level.get_tasks())

    def test_get_points(self):
        """
        Test getter for number of points the level is worth
        """
        level = InterestLevel(1,1)
        self.assertEqual(level._points, level.get_points())

    def test_get_number(self):
        """
        Test getter for the number of the level 
        """
        level = InterestLevel(1,1)
        self.assertEqual(level._number, level.get_number())