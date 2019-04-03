from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Exercise, Programme, Extra
import floppyforms
from django import forms
from Users.fields import ListTextWidget
from django.forms import formset_factory
from bootstrap_datepicker_plus import DatePickerInput
from django.core.exceptions import ValidationError

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

# nested name space for configurations
    class Meta:
        # when form validates its going to create a new User
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists, do you already have an account?")
        return self.cleaned_data

class UserBodyweightForm(forms.ModelForm):

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    class Meta:
        model = Extra
        fields = ['bodyweight', 'date_of_birth']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']


class UserAddDateProgramme(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=True)

    class Meta:
        model = Programme
        fields = ['date']


class UserUpdateExercise(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(), initial=0)

    widgets = {
        'name': floppyforms.widgets.Input(datalist=exercise)
    }
    class Meta:
        model = Exercise
        exclude = ['name']


class UserProgrammeForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(), initial=0)
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=True)
    notes = forms.CharField(required=False)
    # extra_field_count = forms.CharField(widget=forms.HiddenInput())

    widgets = {
        'name': floppyforms.widgets.Input(datalist=exercise)
    }

    class Meta:
        model = Programme
        fields = ['date', 'exercise', 'sets', 'reps', 'weight', 'notes']



class AddExercise(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model=Exercise
        fields= ['name']


