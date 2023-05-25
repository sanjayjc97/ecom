from django import forms 
from .models import *


class Product_add_form(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(Product_add_form,self).__init__(*args,**kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class":"form-control"})

    class Meta:
        model = Product 
        exclude = ['status',"created_on","created_by","slug_field"]