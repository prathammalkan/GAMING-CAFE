from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health_check, name="health"),
    path("browse/", views.browse_games, name="browse"),
    path("games/<slug:slug>/", views.game_detail, name="game-detail"),
    path("games/<slug:slug>/wishlist/", views.toggle_wishlist, name="toggle-wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
]
