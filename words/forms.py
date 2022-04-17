from django import forms

class NameForm(forms.Form):
    searchbar = forms.CharField(label='MetaSearch:', max_length=100)