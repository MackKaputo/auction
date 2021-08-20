from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("newbid/<int:listing_id>", views.newbid, name="newbid"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.this_category, name="this_category"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("closed", views.closed, name="closed"),
    path("closed/<int:listing_id>", views.closed_listing, name="closed_listing"),
] 

