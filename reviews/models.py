from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.db.models.constraints import CheckConstraint
from django.db.models import Q, F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image= models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.headline
    


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_user", null=True)
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by", null=True)
    
    def check_self_following(self):
        if self.user == self.followed_user:
            return False
        return True

    def clean(self):
        if not self.check_self_following():
            raise ValidationError('User can not follow himself')
    
    class Meta:
        unique_together = ('user', 'followed_user')
