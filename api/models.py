#coding:utf-8
from django.db import models

# Create your models here.



class Guest(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=12, unique=True) #嘉宾第二次参加会议时，如果手机号不变，姓名变了，如何处理？
    email = models.EmailField()


class Event(models.Model):
    title = models.CharField(max_length=50, null=False)
    limit = models.IntegerField(default=200)
    status = models.IntegerField(default=0, choices=((0, '未开始'),(1, '进行中'),(2, '已结束')))
    address = models.CharField(max_length=200, null=False),
    time = models.DateTimeField()
    guest = models.ManyToManyField(Guest) # 第三张表手动增加signtime（是否签到）字段



