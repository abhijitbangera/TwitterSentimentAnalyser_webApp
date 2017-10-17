from django import forms

class searchForm(forms.Form):
    Search = forms.CharField(required=True)