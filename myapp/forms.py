from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
 
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('contact',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'pertime', 'cooktime', 'yields', 'ingredients', 'description', 'photo']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'subject', 'email', 'message', 'remark',)