from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)

			if not user:
				raise forms.ValidationError("username and password do not match.")

			# if not user:
			# 	raise forms.ValidationError("I'm sorry. Username does not exist.")
			# if not user.check_password(password):
			# 	raise forms.ValidationError("User password is incorrect.")
			if not user.is_active:
				raise forms.ValidationError("I'm sorry. It seems this user is no longer active.")			
			return super(UserLoginForm, self).clean(*args, **kwargs)			