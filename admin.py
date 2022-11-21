from django.contrib import admin
from auctions.models import Auction, Bid, Comment, Category, User

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)