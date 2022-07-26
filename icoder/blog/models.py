from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True, default=now)
    content=models.TextField()
    img = models.ImageField(upload_to='static', default=0)

    def __str__(self):
        return self.title + ' by ' + str(self.user)
     



class BlogComment(models.Model):
    id= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username

