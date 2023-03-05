from django.contrib.auth.models import AbstractUser
from django.db import models

Categories = (
    'Clothing',
    'Furniture',
    'Electronics',
    'Miscellaneous',
    'Kitchen',
    'None',

)


class User(AbstractUser):
    pass


class List(models.Model):
    title = models.CharField(max_length=64)
    listed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listed_user")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=1, default=Categories[5])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listed_by} has listed {self.title} and priced {self.price}"


class Bid(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="bided_title")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder_user")
    bid = models.DecimalField(max_digits=100, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has bided {self.bid} on {self.list.title}"


class Comment(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="commented_list")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commented_user")
    comment = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has commented {self.comment} on {self.list.title}"


class WatchList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist_user")
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="list")

    def __str__(self):
        return f"{self.user.username} added {self.list.title} to watchlist"
