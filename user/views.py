from django.shortcuts import render

# Create your views here.


import re
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

#local imports 

from .forms import (
    Custom_user_creation_form,
    Custom_auth_form
    )
from base.utils import Manage_base_view



class Login_signup_view(Manage_base_view):

    def login_view(self,request,*args,**kwargs):
        form = Custom_auth_form

        if request.method == "POST":
            form = Custom_auth_form(data = request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = user_name,password = password) 
                if user is not None:
                    login(request,user)
                    return redirect("homepage")
                
        return render(request,"login.html",locals())
    
    def signup_view(self,request,*args,**kwargs):
        form = Custom_user_creation_form
        path  = re.sub('/',"",request.get_full_path())
        if request.method == 'POST':
            form = Custom_user_creation_form(data = request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("homepage")
        return render(request,'login.html',locals())
    

    def logout_view(self,request,*args,**kwargs):
        logout(request)
        return redirect('homepage')
