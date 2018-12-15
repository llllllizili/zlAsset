from django.db import models

# Create your models here.




class User(models.Model):
    username = models.CharField(max_length=128,null=True, blank=True,verbose_name=u"用户名")
    password = models.CharField(max_length=128,null=True, blank=True,verbose_name=u"用户密码")

    def __str__(self):
        return self.username
