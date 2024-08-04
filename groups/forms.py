from django import forms
from .models import Group, GroupPost

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'visibility', 'category', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['content']