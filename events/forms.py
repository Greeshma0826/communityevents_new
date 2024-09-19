# events/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from .models import Event, UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_time', 'end_time', 'image']

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect,
        required=False
    )
    

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        min_length=8,
        help_text="Your password must be at least 8 characters long."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter the same password as above, for verification."
    )
    email = forms.EmailField(
        required=True,
        validators=[validate_email],
        help_text="Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_category']  # Ensure this matches your model's fields
