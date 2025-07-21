from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Appointment,Doctor

from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor


class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'specialty', 'phone', 'availability']

    def clean_email(self):
        email = self.cleaned_data['email']
        # Prevent duplicates, but allow current user
        if self.instance and self.instance.pk:
            if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        doctor = super().save(commit=False)
        user_data = {
            'email': self.cleaned_data['email'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
        }

        if not self.instance.pk:
            # New doctor: create user
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                password=self.cleaned_data['email'],  # Or generate secure password
                role=2
            )
            doctor.user = user
        else:
            # Update existing user
            user = doctor.user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

        if commit:
            doctor.save()
        return doctor

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        (1, 'Patient'),
    )

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial=1, widget=forms.HiddenInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'role',
            'date_of_birth', 'gender', 'phone', 'address',
            'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs.update({'class': css_class})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username as email
        user.email = self.cleaned_data['email']     # Make sure email is saved too
        # Set role to Patient (1)
        user.role = 1  # Make sure your User model supports this field
        if commit:
            user.save()
        return user



# class DoctorForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     email = forms.EmailField()

#     class Meta:
#         model = Doctor
#         fields = ['first_name', 'last_name', 'email', 'specialty', 'phone', 'availability']

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         # Prevent duplicates when adding (but skip if updating)
#         if self.instance and hasattr(self.instance, 'user'):
#             if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
#                 raise forms.ValidationError("Email already exists")
#         else:
#             if User.objects.filter(email=email).exists():
#                 raise forms.ValidationError("Email already exists")
#         return email

#     def save(self, commit=True):
#         doctor = super().save(commit=False)
#         if not self.instance.pk:  # only on create
#             user = User.objects.create_user(
#                 username=self.cleaned_data['email'],
#                 email=self.cleaned_data['email'],
#                 first_name=self.cleaned_data['first_name'],
#                 last_name=self.cleaned_data['last_name'],
#                 password=self.cleaned_data['email'],
#                 role=2
#             )
#             doctor.user = user
#         else:
#             user = doctor.user
#             user.first_name = self.cleaned_data['first_name']
#             user.last_name = self.cleaned_data['last_name']
#             user.email = self.cleaned_data['email']
#             user.save()

#         if commit:
#             doctor.save()
#         return doctor

# Appointment form for booking
class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Appointment Date and Time"
    )

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
