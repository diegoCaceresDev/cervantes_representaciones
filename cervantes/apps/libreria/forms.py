from django import forms

class book_form(forms.Form):
    first_name = forms.CharField(max_length=100, label="First name")
    last_name = forms.CharField(max_length=100, label="last_name")
    date = forms.DateField(required=False, label="date")
    phone = forms.IntegerField(label="phone")
    title = forms.CharField(max_length=100, label="title")
    price = forms.IntegerField(label="price")

