from typing import Any
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from game.models import GameManager

#CustomerUserManager used to create our types of users, extends the base UserManager
class CustomUserManager(UserManager):

    #Base method we use to create a user, 
    def _create_user(self, email, password, **kwargs):
        #Ensures an email is enetered
        if not email:
            raise ValueError("You have not provided a valid e-mail address.")
        #Normalizes email to make matching inputs easier
        email = self.normalize_email(email)
        #Uses normalized email and rest of parameters to create a new user instance
        user = self.model(email=email, **kwargs)
        #Sets the password for the user
        user.set_password(password)

        #Saves the user to out database
        user.save(using=self._db)

        return user
    
    #Creates a normal user
    def create_user(self, email=None, password=None, **kwargs):
        #Sets the is_staff and is_superuser to false so we know the user is of the lowest tier
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        #Calls the base model and creates a user with the above parameters
        return self._create_user(email, password, **kwargs)
    #Same as above but instead sets both staff and superuser to true, user of highest tier
    def create_superuser(self, email=None, password=None, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True

        return self._create_user(email, password, **kwargs)
        
#Our custom user model
class User(AbstractBaseUser, PermissionsMixin):
    #Fields of our user model
    email = models.EmailField(unique=True)

    username = models.CharField(max_length=30, unique=True, default="")
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")

    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    tasks_till_next = models.IntegerField(default=1)
    GAME_MANAGER = None

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    #Fields we use for authentication
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    #Relationship model with group
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to these groups.',
    )
    #Relationship model with permission
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    #Methos used for getting the full name of  auser, The first and last name combined
    def get_full_name(self):
       return f"%s %s" % (self.first_name, self.last_name)
    #Same as above, but just the first name
    def get_short_name(self):
       return self.first_name or self.email.split('@')[0]

    def get_game_manager(self):
        """
        Gets the game manger object for the user

        Returns
        -------
        GameManager
        The users game manager
        """

        # If not game manager exits one is created 
        if self.GAME_MANAGER is None:
            self.GAME_MANAGER = GameManager(self.points, self.level, self.tasks_till_next)

        # Game manager is returned 
        return self.GAME_MANAGER
    
    def complete_task(self, task):
        """
        Completes a given task for the user

        Parameters
        ----------
        task : String
            The tasks that is being completed
        """
        # If not game manager exists one is created 
        if self.GAME_MANAGER is None:
            self.GAME_MANAGER = GameManager(self.points, self.level, self.tasks_till_next)

        # Tasks is completed and attributed are updated
        self.level, self.points, self.tasks_till_next = self.GAME_MANAGER.complete_task(task)
        self.save()