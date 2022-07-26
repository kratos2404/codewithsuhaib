from django import forms
from .models import Post
#DataFlair
class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class UserPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug','content']


