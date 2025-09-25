from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Posts(models.Model):
    newpost=models.TextField()
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="Allposts")
    likes = models.IntegerField(default=0)
    liked_by=models.ManyToManyField(User,related_name="likedpost",blank=True)
    timestamp= models.DateTimeField(auto_now_add=True)




class Follow(models.Model):
    following= models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    

    def __str__(self):
        return f"{self.follower} is follows {self.following}" 










    
















