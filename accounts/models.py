from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver 

# Create your models here.
#BaseManager class is responsible for creating users,superuser we are trying to customize it using
#UserManager custom class
class UserManager(BaseUserManager):
    # create a user
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        
        user=self.model(
            email=self.normalize_email(email), #normalized means lowercase the email
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        #using parameter is used to define the db to be used
        user.save(using=self._db)
        return user

    # creater a superuser
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin= True
        user.is_active=True 
        user.is_staff=True 
        user.is_superadmin=True 
        user.save(using=self._db)
        return user

        
#AbstractBaseUser is responsible for usermodel 
#AbstractUser is responsible to add extra fields to django user model
class User(AbstractBaseUser):
    VENDOR=1
    CUSTOMER=2
    ROLE_CHOICE=(
        (VENDOR,"VENDOR"),
        (CUSTOMER,'CUSTOMER')
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True)
    #Customer Role,Restaurant Owner Role,SuperAdmin Role
    role=models.SmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    #required fields by django user model
    date_joined=models.DateTimeField(auto_now=False, auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True, auto_now_add=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    objects=UserManager()

    def __str__(self):
        return self.email

    def has_perm(self,prem,obj=None):
        return self.is_admin 

    def has_module_perms(self,app_label):
        return True 

    def get_role(self):
        return "Vendor" if self.role==1 else "Customer"

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_photo=models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='users/cover_pictures',blank=True,null=True)
    address_1=models.CharField(max_length=100,blank=True,null=True)
    address_2=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,null=True,blank=True)
    pincode=models.CharField(max_length=6,null=True,blank=True)
    latitude=models.CharField(max_length=50,null=True,blank=True)
    longtitude=models.CharField(max_length=50,null=True,blank=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True, auto_now_add=False)


    def full_address(self):
        return f'{self.address_1}, {self.address_2}'

    def __str__(self):
        return f"{self.user},{self.state},{self.country},{self.city}"



