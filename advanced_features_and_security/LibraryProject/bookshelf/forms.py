from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class SearchForm(forms.Form):
    title = forms.CharField(max_length=200)