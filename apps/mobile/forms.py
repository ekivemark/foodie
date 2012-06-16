__author__ = 'mark'


from django.forms import ModelForm
from django import forms
from models import *

class Phone_Profile_Form(ModelForm):
    """
    Basic Form
    """
    class meta:
        model = phone
        exclude = ()
        include = ('phone',
                   'created',
                   'name',
                   'last_msg',
                   'last_suggested',
                  )

    #    fav_place       = models.CharField(max_length=100,default="", blank=True)
    #   fav_food        = models.CharField(max_length=100, default="", blank=True)
    #   last_food       = models.CharField(max_length=100, default="", blank=True)
    #   access_code     = models.CharField(max_length=5, default="", blank=True)
