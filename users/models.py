from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)
    skill = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    followings = models.ManyToManyField("self", null=True, related_name="p",blank=True, symmetrical=False)
    followers = models.ManyToManyField("self", null=True, blank=True,related_name="f", symmetrical=False)

    def __str__(self):
    	return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

    def message_url(self):
    	return "/messages/{}".format(self.user)

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height >  300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_users', on_delete=models.CASCADE)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_users', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class UserFollowing(models.Model):
    target = models.ForeignKey(User, related_name="target", null=True, blank=True, on_delete=models.CASCADE)

    follower = models.ForeignKey(User, related_name="follower", null=True, blank=True, on_delete=models.CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

class UserFollowed(models.Model):
	user_id_ed = models.ForeignKey(User, related_name="user_id_ed",blank=True,null=True,on_delete=models.CASCADE)
	
	user_followed_by = models.ForeignKey(User, related_name="user_followed_by",blank=True,null=True, on_delete=models.CASCADE)
    # You can even add info about when user started following
	
	created = models.DateTimeField(auto_now_add=True)

