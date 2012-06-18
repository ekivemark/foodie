#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from django.contrib.auth.models import User
import datetime


class Nutrition(models.Model):
    item            = models.CharField(max_length=100,blank=True, default="")
    place           = models.CharField(max_length=100,blank=True, default="")
    calories        = models.DecimalField(max_digits=6,decimal_places=0,blank=True)
    sodium          = models.DecimalField(max_digits=6,decimal_places=0,blank=True)
    carbohydrate    = models.DecimalField(max_digits=6,decimal_places=2,blank=True)
    sugars          = models.DecimalField(max_digits=6,decimal_places=2,blank=True)
    ndb             = models.CharField(max_length=6,blank=True, default="")
    def __unicode__(self):
        return "%s, %s, %s" % (self.place, self.item, self.calories)
