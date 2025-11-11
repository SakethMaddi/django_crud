from django.db import models

# Create your models here.
class usertable(models.Model):
    user_id=models.IntegerField(primary_key=True)
    user_name=models.CharField(max_length=30,null=False)
    user_email=models.EmailField(max_length=50,default="user@gmail.com")
    user_image=models.URLField(default="empty")
    user_password=models.CharField(max_length=12,null=False)