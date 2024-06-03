from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    is_artist = models.BooleanField(default=False, verbose_name="Artist")

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def active_items_count(self):
        return self.item_set.filter(active=True).count()

class Item(models.Model):
    artist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(null=True, default='no-image.svg')
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    bidders = models.ManyToManyField(User, related_name="bidders" ,blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    bid_end_date = models.DateTimeField(default=timezone.now()+timedelta(days=7),null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    bid = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return f"User: {self.bidder}, Item: {self.item}, Bid: {self.bid}"

class Collection(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True, related_name="won_item")
    win_price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Owner: {self.owner}, Item: {self.item}, Win Price: {self.win_price}"

