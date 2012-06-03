#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from twilio.rest import TwilioRestClient
from datetime import datetime, date, timedelta
from time import gmtime, strftime, mktime
from ..intake.models import PatientProfile
from models import SMSAdherenceTransaction
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


def process_adherence_responses():
    # A patient will have a maximum of 15 minutes to respond or the tx will be
    # considered unresponsive.
    processed_messages=[]
    today =date.today()

    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    messages = client.sms.messages.list(to=settings.TWILIO_DEFAULT_FROM,
        date_sent=today)

    # Ee need to sort out all but the latest messages
    # Lets fetch only the ones from today.
    # we would do this filter using the above list command, but it appears,
    # to be broken and we have submitted a bug request to twilio.

    # This will hold today's messages.  we will attach proper date/datetime to
    # twilio's message structure.
    mymessages=[]


    for m in messages:
        #
        mydate_sent = time.strptime(m.date_sent, "%a, %d %b %Y %H:%M:%S +0000")
        m.mydatetime = datetime(*mydate_sent[0:6])
        m.mydate = date(*mydate_sent[0:3])
        m.myfrom_ =m.from_[2:5] + "-" + m.from_[5:8] + "-" + m.from_[8:12]
        fifteen_min_ago = datetime.now() - timedelta(minutes=15)
        if m.mydatetime > fifteen_min_ago:
            mymessages.append(m)

    #now that we are only dealing with recent incoming SMS messages....
    nowtime = datetime.time(datetime.now())
    fifteen_min_ago = datetime.time(datetime.now()-timedelta(minutes=15))
    print fifteen_min_ago
    for m in mymessages:
        #Get all of the today's transactions that have not occurred yet, but should have
        #print m.myfrom_
        transactions = SMSAdherenceTransaction.objects.filter(
            schedule__patient__mobile_phone_number=m.myfrom_,
            reminder_time__lte=nowtime,
            reminder_time__gte=fifteen_min_ago,
            sent=True,
            response_received=False).exclude(schedule__patient__mobile_phone_number__isnull=True).exclude(schedule__patient__mobile_phone_number="")

        for t in transactions:
            ppn= "+1" + t.schedule.patient.mobile_phone_number.replace('-','').replace(' ','')
            if m.from_== ppn:
                #"This incoming message matched the transaction waiting adjudication."
                print t, "This incoming message matched the transaction waiting adjudication."
                t.response_received=True
                t.response_text=m.body
                t.save()
                processed_messages.append({'body':m.body,
                                           'name': m.name,
                                           'to': m.to,
                                           'from_':m.from_,
                                           'date_sent':m.date_sent})
                break;


    return processed_messages