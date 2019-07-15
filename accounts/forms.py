from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import (
    authenticate,
    # mitunim beja in User o farakhani konim
)
from django.contrib.auth.models import User

from .models import Profile

# ba estefade as in method mitunim Model e User ke az built-in hast ro farakhani konim


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری / ایمیل')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    "چنین نام کاربری/ایمیلی وجود ندارد")
            if not user.check_password(password):
                raise forms.ValidationError("پسورد اشتباه است")
            if not user.is_active:
                raise forms.ValidationError("اکانت شما غیر فعال شده است")

            # harchi user vared karde ro to form sabt mikone
            return super(UserLoginForm, self).clean(*args, **kwargs)


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری", help_text="(با استفاده از نام کاربری می توانید به سایت ورود کنید (از حروف انگلیسی استفاده کنید")
    first_name = forms.CharField(label="نام", required=False)
    last_name = forms.CharField(label="نام خانوادگی", required=False)
    email = forms.EmailField(label="ایمیل", required=True)
    email2 = forms.EmailField(label="تکرار ایمیل")
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput,
                                help_text="رمزعبور انتخابی باید بیش از 8 حرف باشد\n بهتر است رمز عبور شامل حرف/عدد/کاراکتر باشد")
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput,
                                help_text="رمز عبور وارد کرده را دوباره تکرار کنید")

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'email2',
            'password1',
            'password2',
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email and email2 and email != email2:
            raise forms.ValidationError("ایمیل ها باید یکسان باشند")
        # Check mikone ke in email ghablan estefade nashude bashe
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("این ایمیل قبلا استفاده شده")
        return email2

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'phone',
            'city',
            'address',
            'image',
            'post_code'
        ]
