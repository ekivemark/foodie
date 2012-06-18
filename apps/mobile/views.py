__author__ = 'mark'

from models import phone, phone_history
from datetime import datetime, date
from forms import Phone_Profile_Form
from django.shortcuts import render_to_response, RequestContext, HttpResponse

import json
import random
def Check_For_Number(phone_number=""):
    """
    Receive a phone number - check against the phone number log
    Return record if found  otherwise return False
    """

    if phone_number=="":
        # nothing to do
        return False

    # test for encoded + ie. %2B
    phone_number=Clean_Number(phone_number)
    phone_number=PrePad_Number(phone_number)


    try:
       p = phone.objects.filter(phone=phone_number)[:1]
    except:
        return False

    print p
    return p


def Add_Number(phone_number=""):

    if phone_number=="":
        #nothing to do
        return

    phone_number= Clean_Number(phone_number)
    phone_number= PrePad_Number(phone_number)

    # We need a random access code generated
    random_number = random.randrange(10000,99999)
    print phone_number,":", random_number

    p = phone(phone= phone_number,
              created = datetime.now(),
              name = "",
              access_code = random_number
    )
    p.save()


    return p

def Update_Number_Profile(api_dict={}):
    """
    Get data from api_dict
    Update phone record
    Write new record to History file

    """

    if api_dict=={}:
        # Nothing to do
        return False

    print "Updating Profile with ", api_dict

    return api_dict


def Get_Profile(phone_number=""):

    if phone_number=="":
    #nothing to do
        return

    phone_number=Clean_Number(phone_number)

    phone_number=PrePad_Number(phone_number)

    # Lookup Number and return profile

    try:
        p = phone.objects.get(phone=phone_number)
    except:
        return

    print p
    return p



def Clean_Number(phone_number=""):
    """
    Twilio sends numbers through with URLEncoding
    So + = %2B. We need to clean the number before committing to the database

    """

    if phone_number=="":
    # nothing to do
        return phone_number

    print "Before Conversion:",phone_number
    # test for encoded + ie. %2B
    if phone_number.startswith("%2B"):
        phone_number = "+"+phone_number[3:]
        print "After Conversion:",phone_number

    return phone_number

def PrePad_Number(phone_number=""):
    """
    clean spaces from phone_number
    """

    if phone_number=="":
        #nothing to do
        return

    print phone_number
    phone_number_new = phone_number.replace(" ",'')

    print phone_number_new

    return phone_number_new

def Get_History(phone_number=""):
    """
    Lookup in history file and return values

    """

    if phone_number=="":
    # nothing to do
        return phone_number

    phone_number=Clean_Number(phone_number)
    phone_number=PrePad_Number(phone_number)



    # Lookup Number and return profile

    try:
        p = phone_history.objects.filter(phone=phone_number)
    except:
        return

    print p
    return p


def Show_Profile(request,phone_number=""):
    """
    Show a record
    """

    print "in show_profile:",phone_number
    if phone_number=="":
    # nothing to do
        jsonstr = {'code':404,
                   'message': "Not Found"}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/plain")


    phone_number=Clean_Number(phone_number)
    phone_number=PrePad_Number(phone_number)

    p = phone.objects.get(phone=phone_number)
    print "Info for:",p

    form = Phone_Profile_Form(instance=p)

    print form
    context={'form':form,
             'phone': p }

    return render_to_response('mobile/phone.html',
                            context,
                            RequestContext(request))
