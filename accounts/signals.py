from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver 
from .models import User,UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender,instance,created,**kwargs):
    #created flag will return True when action is performed User is created once user is created
    # we need to create userprofile
    print(created)
    if created and not UserProfile.objects.filter(user=instance).exists():
        UserProfile.objects.create(user=instance)
        # print('create the user profile')
        # print('user Profile is created')
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except Exception as e:
            #if userprofile doesn't exists then we will create the userprofile
            UserProfile.objects.create(user=instance)
            print('UserProfile did not exists i created one')
        print('User is updated')

# @receiver(pre_save, sender=User)
# def pre_save_profile_receiver(sender,instance,**kwargs):
#     print(f'User {User.username }is going to be created Now')

# first way to connect sender and reciever
# post_save.connect(post_save_create_profile_reciever,sender=User)