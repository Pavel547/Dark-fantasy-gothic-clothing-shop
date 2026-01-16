from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=250, required=True, widget=forms.EmailInput(attrs={'placeholder': 'EMAIL'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'FIRST NAME'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'LAST NAME'}))
    password1 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD1'}))
    password2 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD2'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        
    
    def clean_email(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('User with this email is already exists')
        return data
        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, max_length=250, widget=forms.EmailInput(attrs={'placeholder': 'EMAIL'}))
    password = forms.CharField(required=True, max_length=250, widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD'}))

    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        self.user_cache = authenticate(self.request, email=email, password=password)
        
        if self.user_cache is None:
            raise forms.ValidationError('Invalid password or email')
        elif not self.user_cache.is_active():
            raise forms.ValidationError('User is inactive')
        return self.cleaned_data
    
    
class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=250, required=False, widget=forms.EmailInput(attrs={'placeholder':'EMAIL'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'FIRST NAME'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'LAST NAME'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'COUNTRY'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'CITY'}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'ADDRESS'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder':'POSTAL CODE'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code']
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('User with this email is already exists')
        return self.cleaned_data
    
    
    def clean(self):
        cleaned_data = self.clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email
        
        for field in ['country', 'city', 'postal_code', 'address']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
