#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from twilio.rest import TwilioRestClient
from datetime import datetime, date, timedelta
from time import gmtime, strftime, mktime
import time

def send_sms_twilio(twilio_body, twilio_to,
                    twilio_from=settings.TWILIO_DEFAULT_FROM):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

    print twilio_to
    if twilio_to=="999-999-9999":
        # Dummy mobile number do not send to Twilio

        d = {'twilio_id':'dummy',
             'from': twilio_from,
             'to': twilio_to,
             'body': twilio_body
        }
    else:
        message = client.sms.messages.create(to=twilio_to,
            from_=twilio_from,
            body=twilio_body)
        d = {'twilio_id': message.name,
             'from_':message.from_,
             'to': message.to,
             'body': message.body}


    #print "To:"+twilio_to
    #print "From:"+twilio_from
    #print "Message:"+twilio_body


    return d

def get_messages():
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    smsmessages=[]

    messages =client.sms.messages.list()
    pp=PatientProfile.objects.exclude(mobile_phone_number__isnull=True).exclude(mobile_phone_number="")
    for patient in pp:
        for message in messages:
            ppn= "+1" + patient.mobile_phone_number.replace('-','').replace(' ','')
            if message.from_ == ppn:
                smsmessages.append(message.body)
    return smsmessages


