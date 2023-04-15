from django import forms
#Add model
from App_Login.models import User, Profile
#Add Builtin Form
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'password1', 'password2',]    

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['user',]