from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):

   class Meta:
      model = Vehicle
      fields = ['vehiclename_id','vehiclenumber','vin','year','price','des','cc','image1','image2','image3']
      #fields = ['image']
