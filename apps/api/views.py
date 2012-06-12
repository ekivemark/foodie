__author__ = 'mark'


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
import re
import os, uuid, json

from forms import *
from utils import send_sms_twilio
# import twilio.twiml

#@login_required
#@access_required("tester")
def sms_send(request):

    print "in the send"

    print request.GET
    print request.POST
    

    if request.method == 'POST':

        form = SMSSendForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "SMS Sent.")
            return render_to_response('smsreminders/send.html',
                    {'form': SMSSendForm()},
                context_instance = RequestContext(request))
            #the form has errors
        return render_to_response('smsreminders/send.html',
                {'form': form},
            context_instance = RequestContext(request))

    #request is a GET (not a POST)
    return render_to_response('smsreminders/send.html',
            {'form': SMSSendForm()},
        context_instance = RequestContext(request))


#@login_required
#@access_required("tester")
def sms_messages(request):


    print "in Messages"


    smsmessages=get_messages()
    return render_to_response('smsreminders/messages.html',
            {'smsmessages': smsmessages},
        context_instance = RequestContext(request))



def incoming(request):
    """
The incoming message from Twilio looks like this:

[03/Jun/2012 18:18:28]
"GET /?AccountSid=ACe6fcd771d89671dc416bb2f07db4cea9
&Body=mcdonalds
&ToZip=21201
&FromState=WV
&ToCity=BALTIMORE
&SmsSid=SMcde5329bb1a0661b229812ff3319c91f
&ToState=MD
&To=%2B14107093335
&ToCountry=US
&FromCountry=US
&SmsMessageSid=SMcde5329bb1a0661b229812ff3319c91f
&ApiVersion=2010-04-01
&FromCity=MORGANTOWN
&SmsStatus=received
&From=%2B13046853137
&FromZip=25411
HTTP/1.1"
200 1000

    """

    print "In incoming"

    # step 1 - Get the number and the message
    try:
        from_number = request.GET['From']
        message = request.GET['Body']
    except:
        print "Nothing passed to incoming"
        from_number = ""
        message = ""

        jsonstr = {'code':200,
                   'message': "Empty Message"}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/plain")

    print request.GET

    print "From:", from_number
    print "Body:", message


    # Now test for Help
    help_result = Parse_For_Help(message, from_number)

    if help_result == True:
        # We had a help request - nothing more to do so return
        print "Help Result:",help_result
        jsonstr = {'code':200,
                   'message': "Help requested from:"+from_number+":"+message}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/plain")


    # We have to evaluate the message

    restaurant_result = Parse_For_Restaurant(message, from_number)

    print "Restaurant Result:[", restaurant_result,"]"
    if restaurant_result == None:
        # We didn't match on a restaurant
        send_back = "Sorry, we don't know where you are. Tell us the Fast Food Restaurant and meal you want to check. eg. McDonalds Big Mac"
        twilio_body = send_back
        send_sms_twilio(twilio_body, from_number, settings.TWILIO_DEFAULT_FROM)
        jsonstr = {'code': 404,
                   'message': "From: "+from_number+":"+message,
                   'error': send_back}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=404, mimetype="text/plain")


    # If we get here we need to check for diet type then meal to compare


    # message = "Big Mac has 563 Calories. Try a Cheeseburger (313), or a Hamburger (265) and be LessBadd!"
    # message = "Get the Small Fries! Thanks for being LessBadd!"

    # twilio_body = message
    # print "Want to send this:",twilio_body
    # resp = send_sms_twilio(twilio_body, from_number, settings.TWILIO_DEFAULT_FROM)
    # send_sms_twilio(twilio_body,from_number, settings.TWILIO_DEFAULT_FROM)
    # print resp

    jsonstr = {'code':200,
               'message': "From:"+from_number+": At:"+restaurant_result.title()+"["+message+"]"}
    jsonstr = json.dumps(jsonstr, indent=4,)
    return HttpResponse(jsonstr, status=200, mimetype="text/plain")


def Parse_For_Help(body_text="", return_number=""):
    """
    Body from SMS via Twilio needs to be parsed and action taken

    Return False if no request for help
    Otherwise return True
    """

    if body_text == "":
        # Nothing to do
        return False

    # we have something to process
    # force to lowercase

    text_to_parse = Text_To_List(body_text)

    detailed_help = False
    step = 0
    getting_help = False
    result = ""
    for i in range(len(text_to_parse)):

        word = text_to_parse[i]
        print i
        if word=="help" or word=="?" or word=="help?":
            if len(text_to_parse)==1:
                # Just help sent so send a basic response
                print "You asked for help using this command: ",word
                help_text = "text name of fast food place &, optionally, diet you follow & item you are thinking of. We will send an alternative. BmoreGood.com"

                if return_number !="":
                    result = send_sms_twilio(help_text, return_number, settings.TWILIO_DEFAULT_FROM)
                    print result
                return True
            else:
                detailed_help = True
                # There is more to process. We need to give a detailed help response

        elif i>=1:
            if word=="diet" or word=="diettype" or word=="diet-type":
                # Send help on diet
                print "You asked for help on diet: ", word
                help_text = "diet type tailors suggestions to suit your diet(if possible):Options LowSodium,GlutenFree,LowCal. BMoreGood.com"
                if return_number !="":
                    result = send_sms_twilio(help_text, return_number, settings.TWILIO_DEFAULT_FROM)
                    print result
                return True

    # if drop to this point we have not dealt with any help text
    # so return False
    return False


def Parse_For_Restaurant( body_text="", return_number=""):


    text_to_parse = Text_To_List(body_text)

    fast_food_place = ""
    matched_place = False
    for i in range(len(text_to_parse)):
        word = text_to_parse[i]
        fast_food_place = fast_food_place+word
        print "Step:",i," check for Fast Food Place: ",fast_food_place
        # search fast food places
        matched_place = Lookup_Restaurant(fast_food_place)
        # if more than one entry returned check with second word
        print "Matched: ",matched_place

        if matched_place == False:
            fast_food_place = fast_food_place+" "
        else:
            return fast_food_place


    return


def Text_To_List(body_text=""):
    """
    Receive a text string force to lower case
    and convert to a list breaking on the whitespace
    """

    text_to_parse = re.split('\W+',body_text.lower())

    print "body text:", text_to_parse
    print "Items:", len(text_to_parse)

    return text_to_parse

def Lookup_Restaurant(food_joint=""):
    """
    Lookup Fast Food Place in list and return if a unique entry found
    """

    # Do lookup
    # We need to check for derivations of names
    # eg. McDonalds, Mc Donalds, McD, MickeyD

    if food_joint == "taco bell":
        return True


    return False