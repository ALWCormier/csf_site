from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Enter a message", widget=forms.Textarea)
