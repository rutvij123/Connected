from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django_mysql.models import ListCharField


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	college = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)
	bio = models.TextField(max_length = 1000)
	birth_date = models.CharField(max_length = 100)
	#followers = models.ListCharField(base_field= models.CharField(max_length= 50), size=100, max_length=5500)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Followers(models.Model):
	profile = models.ForeignKey(Profile, on_delete= models.CASCADE)
	follower_name = models.CharField(max_length= 50)

class Following(models.Model):
	profile = models.ForeignKey(Profile, on_delete= models.CASCADE)
	following_name = models.CharField(max_length= 50)	

class Post(models.Model):
	heading =models.TextField(max_length=100)
	content  = models.TextField(max_length=5000)
	profile = models.ForeignKey(Profile, on_delete= models.CASCADE, blank=True)

class Comments(models.Model):
	post = models.ForeignKey(Post, on_delete =models.CASCADE, blank=True)
	content = models.TextField(max_length=5000)
	commenter = models.TextField(max_length=50)	

	

