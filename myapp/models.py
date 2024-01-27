from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Recipe(models.Model):
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    pertime = models.CharField(max_length=200, null=True, blank=True)
    cooktime = models.CharField(max_length=200, null=True, blank=True)
    yields = models.CharField(max_length=200, null=True, blank=True)
    ingredients = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    photo = models.FileField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

STATUS = ((1, "Waiting For Approval"), (2, "Approval"), (3, 'Rejected'))
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    message = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="unread", null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class About(models.Model):
    pagetitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.pagetitle

class Contact2(models.Model):
    pagetitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.pagetitle
