from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    points = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='player_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this player belongs to. A player will get all permissions granted to these groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='player_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this player.',
        related_query_name='player',
    )

    class Meta:
        verbose_name_plural = "Players"

    def __str__(self):
        return self.username
