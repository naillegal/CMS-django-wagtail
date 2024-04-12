from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import PostPage,Tag,BlogCategory
from django.utils import timezone

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User


class BlogForm(forms.ModelForm):
    title = forms.CharField(required=True)
    header_image = forms.ImageField(required=True)
    paragraph = forms.CharField(widget=forms.Textarea, required=False)
    image_text_caption1 = forms.CharField(required=False)
    image_text_1 = forms.ImageField(required=False)
    image_text_caption2 = forms.CharField(required=False)
    image_text_2 = forms.ImageField(required=False)
    quotes = forms.CharField(widget=forms.Textarea, required=False)
    quotes_by = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False) 
    categories = forms.ModelMultipleChoiceField(queryset=BlogCategory.objects.all(), required=False) 
    file = forms.FileField(widget=forms.FileInput,required=False)

    class Meta:
        model = PostPage
        fields = ['title', 'header_image', 'paragraph', 'image_text_caption1', 'image_text_1', 'image_text_caption2', 'image_text_2', 'quotes', 'quotes_by', 'tags', 'categories', 'file']

