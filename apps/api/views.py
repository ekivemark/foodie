__author__ = 'mark'


from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
import re
import os, uuid, json
from ..mobile.views import Check_For_Number, Add_Number, Clean_Number, Get_Profile
from ..nutrition.models import Nutrition

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


    # Developing a dictionary to handle the parsed Twilio message
    api_date =
    {'from_number':from_number,
     'new_number': True,
     'body_word_count':0,
     'body_message_original': "",
     'body_message_lower':"",
     'body_word_list':parsed_body_list,
     'help_word_count':0,
     'help_words': help_result,
     'help_word_list':parsed_help_list,
     'diet_word_count':0,
     'diet_word_list':parsed_diet_list,
     'diet_words': diet_result,
     'diet_message':"",
     'diet_match': False,
     'place_word_count':0,
     'place_words':"",
     'place_word_list':parsed_place_list,
     'place_message':"",
     'place_match': False,
     'food_word_count':0,
     'food_words': food_result,
     'food_word_list':parsed_food_list,
     'food_message':"",
     'food_match':False,
     }

    """


    api_data = {'from_number':"",
                'new_number': True,
                'body_word_count':0,
                'body_message_original': "",
                'body_message_lower':"",
                'body_word_list':[],
                'help_word_count':0,
                'help_words': "",
                'help_message':"",
                'help_word_list':"",
                'diet_word_count':0,
                'diet_word_list':"",
                'diet_words': "",
                'diet_message':"",
                'diet_match': False,
                'food_word_count':0,
                'food_words': "",
                'food_word_list':"",
                'food_message':"",
                'food_match': False,
                'place_word_count':0,
                'place_word_list':"",
                'place_words':"",
                'place_message':"",
                'place_match': False,
                }
    print "In incoming"

    # step 1 - Get the number and the message
    try:
        from_number = request.GET['From']
        message = request.GET['Body']

        api_data['from_number'] = from_number
        api_data['body_message_original'] = message
    except:
        print "Nothing passed to incoming"

        api_data['from_number']  = ""
        api_data['body_message_original'] = ""

        jsonstr = {'code':404,
                   'message': api_data}
        jsonstr = json.dumps(jsonstr, indent=4,)

        return HttpResponse(jsonstr, status=404, mimetype="text/json")


    print request.GET

    print "From:", from_number
    print "Body:", message

    # Now we setup the message for processing
    api_data['body_message_lower'] = message.lower()
    api_data['body_word_list'] = Text_To_List(message.lower())

    # Check if a known number

    number_result = Check_For_Number(from_number)
    print "Check for Number returned:", number_result

    # Pull profile for known number and add to dictionary
    if number_result != False:
        number_profile = Get_Profile(from_number)
        print number_profile

    if number_result != from_number:
        print "there is no record of that number:",from_number
    if from_number!="" and number_result!="":
        create_profile_result = Add_Number(from_number)
        print create_profile_result


    # Add Dispatcher routine here



    # Number passed with no Body
    # Send a welcome message in response

    if message == "":
        api_data['help_message']="Welcome to BMoreGood.com. Send HELP or Fast Food Place and what you want to eat and we will give you a healthier suggestion."
        if from_number != "":
            send_sms_twilio(api_data['help_message'], from_number, settings.TWILIO_DEFAULT_FROM)
        jsonstr = {'code':200,
                   'message': api_data}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/json")

    # Test for Profile - save settings. eg. Diet
    # Test for Help


    # Now test for Help
    api_data_return = Parse_For_Help(api_data)
    if api_data_return != {}:
        api_data = api_data_return

    if api_data['help_word_count']==0:
        help_result = False
    else:
        help_result = True

    if help_result == True:
        # We had a help request - nothing more to do so return
        print "Help Result:",api_data_return
        jsonstr = {'code':200,
                   'message': api_data}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/json")


    # We have to evaluate the message

    restaurant_result = None
    api_data_return = Parse_For_Restaurant(api_data)
    if api_data_return != {}:
        api_data = api_data_return
        restaurant_result = api_data['place_words']


    print "Restaurant Result:", restaurant_result,"."
    if restaurant_result == None and from_number!="":
        # We didn't match on a restaurant
        send_back = "Sorry, we don't know where you are. Tell us the Fast Food Restaurant and meal you want to check. eg. McDonalds Big Mac"
        api_data['place_message'] = send_back
        send_sms_twilio(send_back, from_number, settings.TWILIO_DEFAULT_FROM)
        jsonstr = {'code': 404,
                   'message': api_data,
                   'error': send_back}
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=404, mimetype="text/json")


    # If we get here we need to check for diet type then meal to compare
    # first we strip the restaurant_result from the initial
    diet_result = None
    api_data_return = Parse_For_Diet(api_data)
    if api_data_return != {}:
        api_data = api_data_return
        diet_result = api_data['diet_words']


    # After assessing Diet guide we need to check for food choice and pick an alternative
    food_result = None
    api_data_return = Parse_For_Food(api_data)
    if api_data_return != {}:
        api_data = api_data_return
        food_result = api_data['food_words']
        print food_result
        food_message = api_data['food_message']


        if food_message != "" and from_number !="":
            # send the Twilio message
            send_back = api_data['food_message']
            send_sms_twilio(send_back,from_number, settings.TWILIO_DEFAULT_FROM)
            jsonstr = {'code': 200,
                       'message': api_data,
                       }
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(jsonstr, status=200, mimetype="text/json")

    # if there is no food choice to compare against then we need to pull the
    # food options for the restaurant and make a suggestion.

    food_suggestion = None

    food_to_evaluate = Lookup_FoodPlace(api_data['place_words'])
    if food_to_evaluate != "" and from_number!="":

        print "Returned List:",food_to_evaluate
        print "=============="
        # send the Twilio message
        send_back = food_to_evaluate
        api_data['food_message']= food_to_evaluate
        send_sms_twilio(send_back,from_number, settings.TWILIO_DEFAULT_FROM)
        jsonstr = {'code': 200,
                   'message': api_data,
                   }
        jsonstr = json.dumps(jsonstr, indent=4,)
        return HttpResponse(jsonstr, status=200, mimetype="text/json")

    # now let's update the History and the Phone Record

# Our work here is done. Tidy up and be on our way.

    # message = "Big Mac has 563 Calories. Try a Cheeseburger (313), or a Hamburger (265) and be LessBadd!"
    # message = "Get the Small Fries! Thanks for being LessBadd!"


    # api_data = json.dumps(api_data, indent=4)


    jsonstr = {'code':200,
               'message': api_data,
               'error': "",
               }
    jsonstr = json.dumps(jsonstr, indent=4)
    return HttpResponse(jsonstr, status=200, mimetype="text/json")



def Parse_For_Help(api_dict={}):
    """
    Body from SMS via Twilio needs to be parsed and action taken

    Return False if no request for help
    Otherwise return True

    """

    if api_dict == {}:
        # Nothing to do
        return api_dict

    # we have something to process
    # force to lowercase

    body_text = api_dict['body_message_original'].lower()
    api_dict['body_message_lower'] = body_text
    text_to_parse = Text_To_List(body_text)
    api_dict['body_word_list'] = text_to_parse
    return_number = api_dict['from_number']

    help_words = ""
    help_word_list = []
    detailed_help = False
    step = 0
    getting_help = False
    result = ""

    # if first word indicates help required process help routine
    # otherwise exit the help routine

    if body_text[0]=="?":
        print "Got:",api_dict['body_message_original'][0]
        do_help = True
    elif text_to_parse[0]=="help" or text_to_parse[0]=="help?":
        print "Got:",text_to_parse[0]
        do_help = True
    else:
        print "Not a Help Query"
        do_help = False
        return api_dict


    for i in range(len(text_to_parse)):

        word = text_to_parse[i]
        print i
        if word=="help" or word=="?" or word=="help?":
            if len(text_to_parse)==1:
                # Just help sent so send a basic response
                print "You asked for help using this command: ",word
                help_text = "text name of fast food place &, optionally, diet you follow & item you are thinking of. We will send an alternative. BmoreGood.com"
                api_dict['help_message'] = help_text
                help_words = help_words + word
                api_dict['help_words'] = word

                help_word_list.append(word)

                api_dict['help_word_count'] = len(help_word_list)
                api_dict['help_word_list']  = help_word_list

                if return_number !="":
                    result = send_sms_twilio(help_text, return_number, settings.TWILIO_DEFAULT_FROM)
                    print result

                return api_dict
            else:
                detailed_help = True
                help_words = help_words = word + " "
                help_word_list.append(word)
                # There is more to process. We need to give a detailed help response

        elif i>=1:
            if word=="diet" or word=="diettype" or word=="diet-type":
                if detailed_help == True:
                    help_words = help_words + word
                    help_word_list.append(word)
                    api_dict['help_word_list'] = help_word_list
                # Send help on diet

                print "You asked for help on diet: ", word
                help_text = "diet type tailors suggestions to suit your diet(if possible):Options LowSodium,GlutenFree,LowCal. BMoreGood.com"
                api_dict['help_message'] = help_text
                api_dict['help_words']   = help_words
                api_dict['help_word_count'] = len(api_dict['help_word_list'])

                if return_number !="":
                    result = send_sms_twilio(help_text, return_number, settings.TWILIO_DEFAULT_FROM)
                    print result

                return api_dict
            else:
                if word=="low" or word=="sodium" or word=="gluten" or word=="free" or word=="cal" or word=="calorie":
                    help_words = help_words + word+" "
                    help_word_list.append(word)
                    api_dict['help_word_list'] = help_word_list
                    api_dict['help_word_count'] = len(help_word_list)

    # if drop to this point we have not dealt with any help text
    # so return False
    return api_dict



def Parse_For_Restaurant( api_dict={}):

    if api_dict == {}:
    # Nothing to do
        return api_dict

    # we have something to process
    # force to lowercase

    body_text = api_dict['body_message_original'].lower()

    text_to_parse = Text_To_List(body_text)

    fast_food_place = ""
    fast_food_word_list = []
    matched_place = False
    for i in range(len(text_to_parse)):
        word = text_to_parse[i]
        fast_food_word_list.append(word)
        fast_food_place = fast_food_place+word
        print "Step:",i," check for Fast Food Place: ",fast_food_place
        # search fast food places

        check_restaurant = Lookup_Restaurant(fast_food_place)
        if check_restaurant!=False:
            matched_place = True
            fast_food_place = check_restaurant

        # if more than one entry returned check with second word
        print "Matched: ",matched_place

        if matched_place == False:
            fast_food_place = fast_food_place+" "
        else:
            api_dict['place_word_count'] = i +1
            api_dict['place_words'] = fast_food_place
            api_dict['place_match'] = matched_place
            api_dict['place_word_list'] = fast_food_word_list
            return api_dict


    if matched_place == False:
        api_dict['place_word_count'] = 0
        api_dict['place_match'] = matched_place

    return api_dict


def Parse_For_Diet(api_dict={}):

    if api_dict == {}:
    # Nothing to do
        return api_dict

    # we have something to process

    # We should have processed the Restaurant so we can use the place_word_count as
    # an offset in to the body_word_list

    print "In Parse_For_Diet, with:"
    print api_dict

    offset = 0
    if api_dict['place_match']==True:
        # if we matched on place in previous step we don't need
        # to reprocess the restaurant name.
        offset = api_dict['place_word_count']

    body_text = api_dict['body_message_original'].lower()
    text_to_parse = Text_To_List(body_text)

    diet = ""
    diet_word_list = []
    matched_diet = False

    for i in range(offset,len(text_to_parse)):
        word = text_to_parse[i]
        diet_word_list.append(word)
        diet = diet+word
        print "Step:",i," check for diet: ",diet
        # search diet

        checked_diet = Lookup_Diet(diet)
        if checked_diet !=False:
            matched_diet = True
            diet = checked_diet

        # if more than one entry returned check with second word
        print "Matched: ",matched_diet

        if matched_diet == False:
            diet = diet+" "
        else:
            api_dict['diet_word_count'] = (i-offset) +1
            api_dict['diet_words'] = diet
            api_dict['diet_match'] = matched_diet
            api_dict['diet_word_list'] = diet_word_list
            return api_dict


    if matched_diet == False:
        api_dict['diet_word_count'] = 0
        api_dict['diet_match'] = matched_diet


    return api_dict

def Parse_For_Food(api_dict={}):

    if api_dict == {}:
    # Nothing to do
        return api_dict

    # we have something to process

    # We should have processed the Restaurant and Diet so we can use the place_word_count
    # and diet_word_count as an offset in to the body_word_list

    print "In Parse_For_Food, with:"
    # print api_dict

    if api_dict=={}:
        # Nothing to do
        return api_dict

    # Something to evaluate

    offset = 0 + api_dict['place_word_count'] + api_dict['diet_word_count']

    body_text = api_dict['body_message_original'].lower()
    text_to_parse = Text_To_List(body_text)

    food = ""
    food_word_list = []
    matched_food = False
    print "Offset:",offset

    i = 0
    for i in range(offset,len(text_to_parse)):
        print i
        word = text_to_parse[i]
        food_word_list.append(word)
        food = food+word
        if i != len(text_to_parse)-1:
            food = food + " "
            print "Food_Word:",food,":"

    # we now have the food to look for


    print "Step:",i," check for food:",food,":"
    # search food

    if food == "":
        checked_food = False
    else:
        checked_food = Lookup_Food_In_Place(api_dict['place_words'],food)

        print "================="
        print food
        print "Found in Nutrition Database"
        print "==========================="
        print checked_food
        print "==========================="

    if checked_food !=False:
        matched_food = True
        food = checked_food
        api_dict['food_word_count'] = (i-offset) +1
        api_dict['food_words'] = food
        api_dict['food_match'] = matched_food
        if food_word_list != []:
            api_dict['food_word_list'] = food_word_list
        api_dict['food_message'] = checked_food
        return api_dict


    if matched_food == False:
        api_dict['food_word_count'] = 0
        api_dict['food_match'] = matched_food


    return api_dict


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

    if   food_joint == "taco bell":
        return "taco bell"
    elif food_joint == "mcdonalds" or food_joint =="mickeyd" or food_joint == "mcd" or food_joint=="mcdonald's":
        return "mcdonald's"
    elif food_joint == "burger king" or food_joint == "bk" or food_joint == "burgerking":
        return "burger king"
    elif food_joint == "kfc" or food_joint == "kentucky fried chicken" or food_joint == "kentuckyfriedchicken":
        return "kentucky fried chicken"

    return False


def Lookup_Diet(diet_word=""):
    """
    Lookup Diet Type
    """

    # Do Lookup
    # We need to allow for derivations of names

    if  diet_word == "low sodium" or diet_word == "low-sodium" or diet_word=="lowsodium":
        return "lowsodium"
    if  diet_word == "low calorie" or diet_word == "low-cal" or diet_word=="low cal" or diet_word == "low calorie":
        return "lowcal"
    if  diet_word == "gluten free" or diet_word == "gluten-free" or diet_word=="glutenfree":
        return "glutenfree"

    return False

def Lookup_FoodPlace(place="", food_word=""):
    """
    Lookup Food in Nutrition database
    """

    if place=="":
        # Nothing to do - we don't know where they are
        return

    print "Looking for food in:",place
    food_choices = Nutrition.objects.filter(place=place.upper).order_by('calories').reverse()

    f = {}         # initialise the output
    key = 'item'    # one of the fields from Nutrition Model

    [f.update({x[key]: x}) for x in [model_to_dict(y) for y in food_choices]]
    print "Now we have this:",f

    # next we iterate over the list.
    # we need to get the heaviest calorie item and the mid one and construct a suggestion

    print "we have ", len(food_choices)," items to evaluate"

    print "Mid point in list is: ",int(round((len(food_choices)+0.4)/2,0))

    cal_counter = 0
    food_message = ""
    for item in food_choices:
        cal_counter = cal_counter +1
        print ">>> ",item.item, item.calories
        if cal_counter ==1:
            item_to_suggest = Slim_Description(item.item,place)
            item_to_suggest = item_to_suggest.title()
            calories_to_suggest = str(item.calories)

            food_message = "It is lower than "+item_to_suggest+" at "+calories_to_suggest+" cals.BmoreGood.com"
        elif cal_counter == int(round((len(food_choices)+0.4)/2,0)):
            item_to_suggest = Slim_Description(item.item,place)
            item_to_suggest = item_to_suggest.title()
            calories_to_suggest = str(item.calories)

            food_message = "Try "+item_to_suggest+" at "+calories_to_suggest+" cals." + food_message


    return food_message


def Lookup_Food_In_Place(place="", food_word=""):
    """
    Lookup Food in Nutrition database
    """

    if place=="":
        # Nothing to do - we don't know where they are
        return

    print "Looking for ",food_word,"food in:",place
    food_choices = Nutrition.objects.filter(place=place.upper,item__contains=food_word.upper).order_by('calories')

    print "found:",food_choices

    f = {}         # initialise the output
    key = 'id'    # one of the fields from Nutrition Model

    [f.update({x[key]: x}) for x in [model_to_dict(y) for y in food_choices]]
    print "Now we have this:",f


    if len(food_choices)>0:
        print "we have food choices:", f

    nutrition_info=f[0]
    print nutrition_info['calories']


    calorie_target = nutrition_info['calories']
    #print calorie_target

    food_message = food_word +" has " + str(calorie_target)+" calories."


    print "Target is to beat:",calorie_target," calories."
    alternate_food_choice = Nutrition.objects.filter(place=place,calories__lte=calorie_target).order_by('-calories').exclude(calories__gte=calorie_target)[0]

    print "alternates are:", alternate_food_choice

    alt_food = alternate_food_choice

    print alt_food.item
    print "!!!!!!!!!!!!!!!!!!!!!"
    print alt_food.calories



    print alt_food.item, "at", alt_food.calories
    food_message = food_message + "Why not try a "+alt_food.item+" at "+alt_food.calories

    saved_calories = int(calorie_target) - int(alt_food.calories)
    food_message = food_message + " and save " + str(saved_calories) + " calories.BmoreGood.com"

    print food_message

    return food_message

def Slim_Description(description="", place=""):
    """
    clean up description for texting
    """

    print "evaluating", description
    print "place info:", place
    if description=="":
        # nothing to do
        return description



    if place == "":
        # don't need to slim down the vendor name
        print "no vendor to eliminate"

    else:
        place = place.lower()
        description = description.lower()
        description = description.replace(place, "")
        # remove punctuation
        description = description.replace(",", " ")

    if len(description) >40:
        description = description[:40]+"..."

    print "slimmed description:", description

    return description
