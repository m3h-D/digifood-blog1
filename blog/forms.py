from django import forms
from tinymce import TinyMCE
from .models import Post, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(label="افزونه", widget=TinyMCEWidget(
        attrs={'required': False, 'cols': 30, 'rows': 10}))
    title = forms.CharField(label="موضوع")
    slug = forms.SlugField(label="نام نوار ادرس")
    image = forms.ImageField(label="تصویر اصلی پست")
    text = forms.CharField(widget=forms.Textarea, label="نوشته اصلی پست")

    special = forms.BooleanField(label="پست ویژه", required=False)

    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'image', 'text', 'content', 'categories', 'special'
        ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'text',
            # 'is_good',
            # 'is_bad',
        ]
