from tkinter import CASCADE
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"

    @property
    def count_active_auctions(self):
        return Auction.objects.filter(category=self).count()

class Auction(models.Model):
    item_name = models.CharField(max_length = 69)
    item_info = models.TextField(max_length = 420)
    item_image = models.ImageField(blank = True, null = True, upload_to ='', editable = True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank = True, null = True)

    start_bid = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])

    ended   = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction")

    watch = models.ManyToManyField(User, blank = True, related_name="watchlist")

    def __str__(self):
        return f"Auction #{self.id}: {self.item_name} ({self.user.username})"

    def is_finished(self):
        if self.ended:
            return True
        else:
            return False


class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid")

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return f"Bid #{self.id}: {self.amount} on {self.auction.item_name} by {self.user.username}"

    
class Comment(models.Model):
    message = models.TextField(max_length = 300)
    time    = models.DateTimeField(auto_now_add=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment")

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return f"Comment #{self.id}: {self.user.username} on {self.auction.item_name}: {self.message}"




