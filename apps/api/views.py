__author__ = 'mark'


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect


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


    print "In incoming"

    # Try adding your own number to this list!
    callers = {
        "+17036232789": "ekivemark",
         }

    """Respond and greet the caller by name."""


    from_number = request.GET['From']
    message = request.GET['Body']

    print request.GET

    print from_number
    print message


    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Big Mac has 563 Calories. Try a Cheeseburger (313 or a hamburger (265)"
        # message = "Get the Small Fries! Thanks for being LessBadd!"


    twilio_body = message

    print "Want to send this:",twilio_body

    resp = send_sms_twilio(twilio_body, from_number, settings.TWILIO_DEFAULT_FROM)

    # send_sms_twilio(twilio_body,from_number, settings.TWILIO_DEFAULT_FROM)

    print resp


    return HttpResponseRedirect('/')







