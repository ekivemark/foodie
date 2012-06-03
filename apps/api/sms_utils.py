#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from twilio.rest import TwilioRestClient


def send_sms_twilio(twilio_body, twilio_to,
                    twilio_from=settings.TWILIO_DEFAULT_FROM):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)


    message = client.sms.messages.create(to=twilio_to,
                                     from_=twilio_from,
                                     body=twilio_body)

    print "Twilio sent ["+str(twilio_body)+"] to "+str(twilio_to)
    return message