from django.urls import path


from . import views

app_name="game"
# The url paths for the game app
urlpatterns = [
    path("", views.game, name="game"),
    path("shop", views.shop, name="shop")
]