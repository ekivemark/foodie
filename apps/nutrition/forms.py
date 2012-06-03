from django import forms
from models import *
import json

class SuggestForm(forms.Form):
    place  = forms.CharField(label="Where are you going?")
    item   = forms.CharField(label="What are you having?")

    def save(self):
        l=[]
        nut = Nutrition.objects.get(place=self.place, item=self.item)
        suggestions = Nutrition.objects.get(place=self.place,
                                            calories__lt=nut.calories)
        for s in suggestions:
            suggestion['item']=s.item
            suggestion['place']=s.place
            suggestion['calories']=s.calories
            l.append(json.dumps(suggestion, indent=4))
        
        return l
