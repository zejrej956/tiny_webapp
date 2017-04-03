from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm

# Create your views here.
def login_view(request):
	form = UserLoginForm(request.POST or None)
	print (request.user.is_authenticated())
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect("/")
		
	context = {
		"form": form
	}
	return render(request, "login_form.html", context)

def logout_view(request):
	logout(request)
	print (request.user.is_authenticated())
	return redirect("/")

# for registration of new user
def register_view(request):
	pass