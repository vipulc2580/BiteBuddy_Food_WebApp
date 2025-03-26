from django import forms 
from .models import User
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(),required=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password','confirm_password']
    
    # any errors which are associated with model fields are called fieldError
    #form bu default calls clean method whenever form is submitted ,to python validate and run valdidators
    # and returns a cleaned_data dictionary
    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError('Password does not match')

    #errors associated with forms cleaned method are NonFieldError(Confirm_password error)