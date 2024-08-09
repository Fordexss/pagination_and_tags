from django import forms
from django.contrib.auth.hashers import make_password

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Repeat password')

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords are not equal')
        return cd.get('password2')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            qs = CustomUser.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User does not exist')
        return cleaned_data


class UpdateProfileForm(forms.ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Repeat password', required=False)

    class Meta:
        model = CustomUser
        fields = ['nickname', 'email']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords are not equal')
        return cd.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ConverterForm(forms.Form):
    from_crypto = forms.ChoiceField(choices=[])
    to_crypto = forms.ChoiceField(choices=[])
    amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ConverterForm, self).__init__(*args, **kwargs)
