from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    bid_value = models.IntegerField()
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="user_bid", null=True)

    def __str__(self):
        return f"bid: {self.bid_value}"

class NewListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=120)
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name ="bid_listing")
    image = models.URLField(max_length= 200, null=True)
    category = models.CharField(max_length=20)
    owner = models.CharField(max_length=25, null=True)

    def __str__(self):
        return f"{self.title}, bid={self.bid}"


class Comment(models.Model):
    text = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="user_comment", default="No User")
    listing = models.ForeignKey(NewListing, on_delete=models.CASCADE, related_name="listing_comment", null=True)
    
    def __str__(self):
        return f"{self.user} commented {self.text}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="user_watchlist", null=True)
    listing = models.ForeignKey(NewListing, on_delete= models.CASCADE, related_name="listing_watchlist", null=True)

class ClosedListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=120)
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name ="closed_bid_listing")
    image = models.URLField(max_length= 200, null=True)
    category = models.CharField(max_length=20)
    owner = models.CharField(max_length=25, null=True)

    def __str__(self):
        return f"{self.title}, bid={self.bid}"
        