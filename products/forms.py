from django import forms
from .models import ProductComment


class CommentForm(forms.ModelForm):

    class Meta:
        model = ProductComment
        fields = [
            'text',
            'is_good',
            'is_bad',
        ]
