from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("cAtegory", views.cAtegory, name="cAtegory"),
    path("listing/<int:id>",views.listing, name="listing"),
    path("add/<int:id>", views.add, name="add"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("close/<int:id>", views.close, name="close"),
    path("wins", views.wins, name="wins"),


]


