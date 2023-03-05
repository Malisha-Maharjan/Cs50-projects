from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("list/<int:list_id>", views.display_list, name="list"),
    path("bid/<int:list_id>", views.place_bid, name="bid"),
    path("comment/<int:list_id>", views.comment, name="comment"),
    path("add_watchlist/<int:list_id>", views.watch_list, name="add_watchlist"),
    path("watchlist/<str:user>", views.display_watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("add_closelist/<int:list_id>", views.close_list, name="add_closelist"),
    path("closedlist", views.display_closed_list, name="closedlist"),
    path("result/<int:list_id>", views.result, name="result")
]
