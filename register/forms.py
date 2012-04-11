from django import forms
from models import Employee, Organization, Task
from django.contrib.auth.models import User

class EmployeeAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    middle_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(EmployeeAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['password'].required = False

            instance = kwargs['instance']
            self.initial['first_name'] = instance.user.first_name
            self.initial['middle_name'] = instance.middle_name
            self.initial['last_name'] = instance.user.last_name
            self.initial['username'] = instance.user.username
            self.initial['email'] = instance.user.email
    
    class Meta:
        model = Employee
        fields = (
            'organization', 'first_name', 'middle_name', 'last_name', 'username',
            'password', 'email'
        )

        
