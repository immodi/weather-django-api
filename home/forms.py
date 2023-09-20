from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label="Enter the city name", max_length=100)