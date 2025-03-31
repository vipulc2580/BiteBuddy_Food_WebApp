from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
from datetime import time,datetime,date
# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    user_profile=models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='userprofile')
    vendor_name=models.CharField(max_length=100)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    vendor_slug=models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            # means this is a update of object
            orig=Vendor.objects.get(pk=self.pk)
            mail_template='accounts/emails/admin_approval_email.html'
            context={
                'user':self.user,
                'is_approved':self.is_approved,
            }
            if orig.is_approved!=self.is_approved:
                if self.is_approved==True:
                    #send notification email
                    mail_subject='Congratulations! Your restaurant has been approved!'
                    send_notification(mail_subject,mail_template,context)
                else:
                    #send notification email
                    mail_subject="We're sorry you are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)
    
    def is_open(self):
        # print('i was invoked')
        today_date=date.today()
        today=today_date.isoweekday()
        current_opening_hours=OpeningHour.objects.filter(vendor=self,day=today)
        now=datetime.now().strftime('%H:%M:%S')
        is_open=False
        for i in current_opening_hours:
            start=str(datetime.strptime(i.from_hour,'%I:%M %p').time())
            end=str(datetime.strptime(i.to_hour,'%I:%M %p').time())
            # print(start,end)
            if now>=start and now<=end:
                is_open=True 
                if i.is_closed:
                    is_open=False
                break
            else:
                is_open=False
        return is_open



class OpeningHour(models.Model):
    days=[
        (1,'Monday'),
        (2,'Tuesday'),
        (3,'Wednesday'),
        (4,'Thursday'),
        (5,'Friday'),
        (6,'Saturday'),
        (7,'Sunday'),
    ]
    HOUR_OF_DAY_24= [
        ('12:00 AM', '12:00 AM'),
        ('12:30 AM', '12:30 AM'),
        ('01:00 AM', '01:00 AM'),
        ('01:30 AM', '01:30 AM'),
        ('02:00 AM', '02:00 AM'),
        ('02:30 AM', '02:30 AM'),
        ('03:00 AM', '03:00 AM'),
        ('03:30 AM', '03:30 AM'),
        ('04:00 AM', '04:00 AM'),
        ('04:30 AM', '04:30 AM'),
        ('05:00 AM', '05:00 AM'),
        ('05:30 AM', '05:30 AM'),
        ('06:00 AM', '06:00 AM'),
        ('06:30 AM', '06:30 AM'),
        ('07:00 AM', '07:00 AM'),
        ('07:30 AM', '07:30 AM'),
        ('08:00 AM', '08:00 AM'),
        ('08:30 AM', '08:30 AM'),
        ('09:00 AM', '09:00 AM'),
        ('09:30 AM', '09:30 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('01:00 PM', '01:00 PM'),
        ('01:30 PM', '01:30 PM'),
        ('02:00 PM', '02:00 PM'),
        ('02:30 PM', '02:30 PM'),
        ('03:00 PM', '03:00 PM'),
        ('03:30 PM', '03:30 PM'),
        ('04:00 PM', '04:00 PM'),
        ('04:30 PM', '04:30 PM'),
        ('05:00 PM', '05:00 PM'),
        ('05:30 PM', '05:30 PM'),
        ('06:00 PM', '06:00 PM'),
        ('06:30 PM', '06:30 PM'),
        ('07:00 PM', '07:00 PM'),
        ('07:30 PM', '07:30 PM'),
        ('08:00 PM', '08:00 PM'),
        ('08:30 PM', '08:30 PM'),
        ('09:00 PM', '09:00 PM'),
        ('09:30 PM', '09:30 PM'),
        ('10:00 PM', '10:00 PM'),
        ('10:30 PM', '10:30 PM'),
        ('11:00 PM', '11:00 PM'),
        ('11:30 PM', '11:30 PM'),
        ]
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day=models.IntegerField(choices=days)
    from_hour=models.CharField(choices=HOUR_OF_DAY_24,max_length=10,blank=True)
    to_hour=models.CharField(choices=HOUR_OF_DAY_24,max_length=10,blank=True)
    is_closed=models.BooleanField(default=False)

    class Meta:
        ordering=('day','-from_hour')
        unique_together=('vendor','day','from_hour','to_hour')

    def __str__(self):
        return self.get_day_display()