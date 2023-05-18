from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group
import os


def customer_profile(sender, instance, created, **kwargs):
    if created: 
        group= Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user= instance, name= instance.username)

post_save.connect(customer_profile, sender= User)


@receiver(pre_save, sender=Customer)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).profile_pic
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    file = instance.profile_pic

    try:
        if not old_file == file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        return False
