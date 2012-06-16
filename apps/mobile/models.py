from django.db import models
from django.conf import settings
from datetime import date, datetime, timedelta

# Create your models here.

class phone(models.Model):
    phone           = models.CharField(max_length=15 )
    created         = models.DateTimeField(blank=True, null=True)
    name            = models.CharField(max_length=50,default="", blank=True)
    fav_place       = models.CharField(max_length=100,default="", blank=True)
    fav_food        = models.CharField(max_length=100, default="", blank=True)
    last_food       = models.CharField(max_length=100, default="", blank=True)
    last_msg        = models.CharField(max_length=200, default="", blank=True)
    last_suggested  = models.CharField(max_length=100, default="", blank=True)
    access_code     = models.CharField(max_length=5, default="", blank=True)
    def __unicode__(self):
        # return "%s, %s, %s" % (self.phone, self.created, self.access_code)
        return "%s" % (self.phone)


class phone_history(models.Model):
    phone           = models.CharField(max_length=15)
    created         = models.DateTimeField(blank=True, null=True)
    message_in      = models.CharField(max_length=200, default="", blank=True)
    message_out     = models.CharField(max_length=200, default="", blank=True)
    calories        = models.IntegerField(null=True)
    calories_saved  = models.IntegerField(null=True)
    def __unicode__(self):
        return "%s, %s, %s" % (self.phone, self.message_in, self.calories)


