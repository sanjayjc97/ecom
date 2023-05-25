from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.views.generic import View
from django.http import Http404

class Status_manager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=True)


class Base_content(models.Model):

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
