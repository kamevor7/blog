from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms

from forum.models import Profile


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'date_joined',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user_Name',
            'first_Name',
            'last_Name',
            'phone_Number',
            'user_Email',
            'address',
            'city',
            'state',
            'zipcode',
        )
