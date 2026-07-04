from django import forms
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','name', 'price', 'description', 'image']
        widgets = {
            'category' : forms.Select(attrs={'class': 'form-select'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control rounded', 'placeholder': 'Enter Product name'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control rounded', 'placeholder':'Enter Price'}),
            'description' : forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder':'Enter description'}),
        }
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})