#save whenever user created
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

"""
    When user is saved, send signal
    Receiver gets signal 
    Receiver is create_profile function
    
    then in function: if User was created:
    make profile of user with the user tied in
    being the instance of the user created
"""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""
    Saves profile after each time user is saved 
"""


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
