from django import forms
from .models import User, Post, Group, GroupPost

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    course = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'course', 'year', 'profile_picture', 'bio', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].required = True
        self.fields['year'].required = True
        
        # Suppress help texts
        for field in self.fields.values():
            field.help_text = ''
        
        # Set bio field to use TextInput widget
        self.fields['bio'].widget = forms.TextInput(attrs={'placeholder': 'Your about'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'course', 'year', 'profile_picture', 'bio', 'privacy_dms', 'privacy_posts']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['content']
