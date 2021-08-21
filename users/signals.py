from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserFollowing ,FriendRequest

@receiver(post_save,sender=UserFollowing)
def post_save_add_to_followers(sender,instance,created , **kwargs):
    
    target = instance.target.profile
    follower = instance.follower.profile
    print("follower :", follower)
    
    print("target : ",target)
    # follower.following.add(target)
    print(follower.following.all())
    # target.followers.add(follower)
    print(target.following.all())
    target.save()
    follower.save()
    print("into the signals")

@receiver(post_save,sender=FriendRequest)
def post_save_add_to_FriendRequest(sender,instance,created , **kwargs):
    print("into the signals FriendRequest")