from django.contrib import admin

from .models import Bid, NewListing, Comment

# Register your models here.

admin.site.register(Bid)
admin.site.register(NewListing)
admin.site.register(Comment)