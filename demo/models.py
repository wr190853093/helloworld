#coding:utf-8
from django.db import models

# Create your models here.
class Author(models.Model):

    name = models.CharField(max_length=32)
    def __unicode__(self):
        return self.name
    # class Meta:
    #     verbose_name = '作者表'
    #     verbose_name_plural = verbose_name


class AuthorDetails(models.Model):
    age = models.IntegerField()
    email = models.CharField(max_length=50)
    sex = models.IntegerField(choices=((0, '男'),(1, '女')))
    phone = models.CharField(max_length=15)
    author = models.OneToOneField(Author)

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    website = models.URLField()
    def __unicode__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=100)
    publication_data = models.DateField()
    publisher = models.ForeignKey(Publisher)
    author = models.ManyToManyField(Author)
    price = models.FloatField()

    def __unicode__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=20)
    pwd = models.CharField(max_length=64)