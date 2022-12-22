from django import forms
from .models import Account,Address
from django.contrib import messages


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number',]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Mobile Number'
        self.fields['phone_number'].widget.attrs['maxlength'] = 10

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control '

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesnot match!!")

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        phone_number = cleaned_data.get('phone_number')
        if type(first_name) != str or type(last_name) != str:
            raise forms.ValidationError("Username is invalid")

        if len(password) < 8:
            raise forms.ValidationError(
                "Passwords must be at least 8 characters long!!")
        if len(phone_number) < 10:
            raise forms.ValidationError("Please enter a valid phone number")


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control '

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=('address_line_1','address_line_2','city','district','state','country','pin_code','primary_address')
    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'