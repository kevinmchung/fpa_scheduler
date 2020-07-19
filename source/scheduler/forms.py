from django import forms
from django.forms import ModelForm
from .models import Name

class NameForm_OLD(forms.Form):
    name_first = forms.CharField(label='First', max_length=50)
    name_last = forms.CharField(label='Last', max_length=50)



class NameForm(ModelForm):

    class Meta:
        model = Name
        fields = ['name_first', 'name_last']