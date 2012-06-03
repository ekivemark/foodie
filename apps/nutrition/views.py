# Create your views here.
import csv
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import *
from forms import SuggestForm
#def loaddata(request):
#    csvfile = csv.reader(open('/home/alan/django-projects/foodie/data/nutrition3.csv', 'rb'), delimiter=',')
#    rowindex = 0
#    for row in csvfile:
#        print row
#
#        doc={}
#        sitem=row[0].split(',')
#        
#        print sitem
#        
#        doc['place'] =sitem[0]
#        print sitem
#        
#        if len(sitem)>1:
#            doc['item'] =sitem[1]
#            doc['calories']=row[1]
#            Nutrition.objects.create(place=doc['place'], item=doc['item'],
#                                 calories=doc['calories'])
#            
#    print "done."

def suggest(request):
    if request.method == 'POST':
        form = SuggestForm(request.POST)

        if form.is_valid():

            suggestions = form.save()
            context = {'suggestions':suggestions }
            return render_to_response('home/suggestions.html', context,
                              RequestContext(request))              
        else:
            messages.error(request, "Oops. The form contains errors.")
            return render_to_response('home/index.html',
                              RequestContext(request,
                                             {'form': form}))
    
    return render_to_response('home/index.html', {'form':SuggestForm()},
                              RequestContext(request))

    