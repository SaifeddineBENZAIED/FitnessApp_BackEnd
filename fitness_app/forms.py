from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account, ReviewOnWebsite

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level', 'phone_number', 'country', 'password']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('is_superuser')
        
        if not user_type:
            # For regular users, ensure phone_number is the only optional field
            required_fields = ['age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'{field} is required')
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class BMICalculatorForm(forms.Form):
    weight_kg = forms.FloatField()
    height_cm = forms.FloatField()

class BMRCalculatorForm(forms.Form):
    weight_kg = forms.FloatField()
    height_cm = forms.FloatField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])

class CalorieNeedsForm(forms.Form):
    weight_kg = forms.FloatField()
    height_cm = forms.FloatField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    activity_level = forms.ChoiceField(choices=[('Sedentary', 'Sedentary'), ('Light', 'Light'), ('Moderate', 'Moderate'), ('Active', 'Active'), ('Very Active', 'Very Active')])

class BodyFatCalculatorForm(forms.Form):
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    waist_cm = forms.FloatField()
    neck_cm = forms.FloatField()
    height_cm = forms.FloatField()
    hip_cm = forms.FloatField(required=False)

class WHRCalculatorForm(forms.Form):
    waist_cm = forms.FloatField()
    hip_cm = forms.FloatField()

class ReviewOnWebsiteForm(forms.ModelForm):
    class Meta:
        model = ReviewOnWebsite
        fields = ['content', 'rating']
