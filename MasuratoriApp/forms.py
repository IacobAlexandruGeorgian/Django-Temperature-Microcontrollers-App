from django import forms
from .models import Tblmasuratori
from crispy_forms.bootstrap import InlineCheckboxes

class MasuratoriSearchForm(forms.ModelForm):
    Start_Date = forms.DateTimeField(required=False)
    End_Date = forms.DateTimeField(required=False)
    class Meta:
        model = Tblmasuratori
        fields = ['Start_Date','End_Date']

class MasuratoriGraficSearchForm(forms.ModelForm):
    The_Date = forms.DateTimeField(required=False)
    class Meta:
        model = Tblmasuratori
        fields = ['The_Date']



