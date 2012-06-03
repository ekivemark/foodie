__author__ = 'mark'


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


from django.forms import ModelForm
from django import forms
from models import *
from django.forms.extras.widgets import SelectDateWidget
import datetime
from datetime import timedelta
this_year = datetime.date.today().year
years = range(this_year-80, this_year-10)
this_year_only= range(this_year, this_year+1)
from utils import send_sms_twilio


class SMSSendForm(forms.Form):
    to      = forms.CharField()
    message = forms.CharField()

    def save(self):
        send_sms_twilio(self.cleaned_data['message'],
            self.cleaned_data['to'])

