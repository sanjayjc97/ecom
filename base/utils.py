from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class Status_manager(models.Manager):
    '''
    a custom manager that will filter out the query for status = True
    '''
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=True)


class Base_content(models.Model):
    '''
    A base class for all the models to inherit from contains the comman fields
    '''
    status_choice = (
                    (True,"Active"),
                    (False,"Inactive")
                    )
    status = models.BooleanField(choices=status_choice,default=True)
    created_on = models.DateTimeField(default=timezone.now)
    update_on = models.DateTimeField(auto_now=True)

    is_active = Status_manager()

    class Meta:
        abstract = True


class Manage_base_view(View):
    '''
    All the views inherit from this view it provides all the basic functionality like get and post 
    '''
    method_name = None
    template_name = None
    items_per_page = 10
    permissions = None

    def get(self,request,*args,**kwargs):
        
        if self.method_name is not None:
            func = getattr(self,self.method_name,None)
            if func is not None:
                return func(request,*args,**kwargs)
        raise Http404('Method not allowed')
    
    
    def post(self,request,*args,**kwargs):
        if self.method_name is not None:
            func = getattr(self,self.method_name,None)
            if func is not None:
                return func(request,*args,**kwargs)
        raise Http404('Method not allowed')




class SuperuserRedirectPermission(UserPassesTestMixin):
    '''
    check if the user is superuser else redirect to homepage
    '''
    def test_func(self):
        user = self.request.user
        if not user.is_superuser:
            return False  # Replace 'home' with the appropriate URL name
        return True
    
    def handle_no_permission(self):
        return redirect('homepage')