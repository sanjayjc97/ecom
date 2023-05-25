from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from django.contrib.auth import get_user_model

class Custom_user_creation_form(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(Custom_user_creation_form,self).__init__(*args,**kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({"class":"form-control"})
            self.fields[name].help_text = " "
    class Meta:
        model = get_user_model()
        fields = ["username","first_name","last_name","password1","password2"]


class Custom_auth_form(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(Custom_auth_form,self).__init__(*args,**kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':"form-control"})


