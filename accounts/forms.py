from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='メールアドレス', required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザー名'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認）'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザー名'
        self.fields['password'].label = 'パスワード'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'avatar', 'prefecture', 'position', 'level')
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'bio': '自己紹介',
            'avatar': 'プロフィール画像',
            'prefecture': '都道府県',
            'position': 'ポジション',
            'level': 'レベル',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
