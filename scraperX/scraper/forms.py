from django import forms
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Username",
        }
    ))
    password    = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Password",
        }
    ))


class RegisterForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Username",
        }
    ))
    email       = forms.EmailField(widget=forms.EmailInput(
        attrs= {
            'class': "form-control",
            'placeholder': "Email",
        }
    ))
    password    = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Password",
        }
    ))
    password2   = forms.CharField(label= "Confirm Password", widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Confirm Password",
        }
    ))


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gamil.com")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password must match.")
        return data

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "First Name",
        }
    ))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Last Name",
        }
    ))
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This is not your email')
        return email