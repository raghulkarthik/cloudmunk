from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from storage.models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
