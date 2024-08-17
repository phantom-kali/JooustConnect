from django import forms
from .models import Group, GroupPost

<<<<<<< HEAD

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "visibility", "category", "tags"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control-dark"}),
            "description": forms.Textarea(attrs={"class": "form-control-dark"}),
            "visibility": forms.Select(attrs={"class": "form-control-dark"}),
            "category": forms.Select(attrs={"class": "form-control-dark"}),
            "tags": forms.TextInput(
                attrs={
                    "class": "form-control-dark",
                    "placeholder": "Enter tags separated by commas",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control-dark"


class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control-dark"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control-dark"
=======
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
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
