from django import forms
from models import *
import json

class SuggestForm(forms.Form):
    place  = forms.CharField(label="Where are you going?")
    item   = forms.CharField(label="What are you having?", required=False)

    def save(self):
        print "jere"
        place = self.cleaned_data.get('place', "")
        item = self.cleaned_data.get('item', "")
        
        #place=place.upper()
        #item=item.upper()
        
        l=[]
        if item:
            print place, item
            nut = Nutrition.objects.filter(place=place, item=item)
        else:
            nut = Nutrition.objects.filter(place=place)
            
        print nut
        
        suggestions = Nutrition.objects.filter(place=place,
                                            calories__lt=nut[0].calories)
        for s in suggestions:
            suggestion={}
            suggestion['item']=s.item
            suggestion['place']=s.place
            suggestion['calories']=s.calories
            l.append(json.dumps(suggestion, indent=4))
        
        return suggestions
