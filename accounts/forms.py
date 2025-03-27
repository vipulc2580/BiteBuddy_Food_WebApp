from django import forms 
from .models import User,UserProfile
from .validators import allow_only_images_validator,validate_file_size

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


class UserProfileForm(forms.ModelForm):
    profile_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator,validate_file_size])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator,validate_file_size])
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing','required':'required'}))
    # one way to make the form field read only
    # latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longtitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model=UserProfile
        fields=['profile_photo','cover_photo','address','country','state','city','pincode','latitude','longtitude']
    
    #second way of making field readonly
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field=='latitude' or field=='longtitude':
                self.fields[field].widget.attrs['readonly']='readonly'