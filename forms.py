from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        })
    )
    roll_no = forms.CharField(
        label='Roll Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. STU001'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    maths = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})
    )
    science = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})
    )
    english = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})
    )
    history = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})
    )
    computer = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})

    )
    biology = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100'})
    )

    class Meta:
        model  = Student
        fields = [
            'name', 'roll_no', 'email',
            'maths', 'science', 'english', 'history', 'computer','biology'
        ]

    def clean_maths(self):
        val = self.cleaned_data.get('maths')
        if val < 0 or val > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return val