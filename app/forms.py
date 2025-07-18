from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Appointment


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


# Doctor creation form (for admin)
class DoctorForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    specialty = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    availability = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save_user(self):
        # Create the User object for the doctor with random password (admin can reset)
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=User.objects.make_random_password(),
            role=2  # Doctor role
        )
        return user


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
