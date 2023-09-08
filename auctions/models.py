from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bid=models.IntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null= True, related_name="userBid")


class Category(models.Model):
    categoryName=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.categoryName}"

class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=1000)
    price=models.ForeignKey(Bid, on_delete=models.CASCADE,blank=True,null=True, related_name="bidPrice")
    isActive=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True, related_name="category")
    owner=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name="owner")
    imageUrl=models.CharField(max_length=10000)
    watchlist=models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name="author")
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True,null=True, related_name="listing")
    message=models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.message}"

