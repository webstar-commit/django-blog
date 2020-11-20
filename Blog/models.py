from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Tag(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    subscribe = models.ManyToManyField(User, related_name="sub_cat",null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=150)

    author = models.ForeignKey(User)

    body = models.TextField()

    image = models.FileField(null=True, blank=True)


    cat = models.ForeignKey(Category, related_name="category_post")

    created_at = models.DateTimeField(auto_now_add=True)

    tag = models.ManyToManyField(Tag)



    def __str__(self):
        return self.title


class Comment(models.Model):

    user = models.ForeignKey(User)

    post = models.ForeignKey(Post)

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)



class BadWord(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



class Reply(models.Model):
    user = models.ForeignKey(User)

    comment = models.ForeignKey(Comment)

    body = models.TextField()

    created_at = models.DateTimeField(default=datetime.now)


class Like(models.Model):

    user = models.ForeignKey(User)

    post = models.ForeignKey(Post)

    state = models.IntegerField()









