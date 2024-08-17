from django import forms
from .models import User, Post

<<<<<<< HEAD

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image", "video"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What's on your mind?",
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control-file"}),
            "video": forms.FileInput(attrs={"class": "form-control-file"}),
        }
=======
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "What's on your mind?"}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'video': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
