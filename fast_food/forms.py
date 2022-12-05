from django import forms
from accounts.models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'profile_pic': forms.FileInput(),
        }
