from django.views.generic import TemplateView,DeleteView,DetailView,ListView ,CreateView, FormView

from django.urls import reverse_lazy
# from app.forms import CustomUserCreationForm, EmailAuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic.edit import UpdateView
from .models import User, Patient, Doctor, Appointment
from .forms import RegisterForm, DoctorForm, AppointmentForm


# Create your views here.
class Home(LoginRequiredMixin,TemplateView):
    template_name='admin/index.html'
class ChartsChartjs(TemplateView):
    template_name='admin/charts-chartjs.html'
class ChartsEharts(TemplateView):
    template_name='admin/charts-echarts.html'
class ComponentsAccordion(TemplateView):
    template_name='admin/components-accordion.html'
class UsersProfile(TemplateView):
    template_name= "admin/users-profile.html"

class FormsValidation(TemplateView):
    template_name='admin/forms-validation.html'
class PagesError404(TemplateView):
    template_name='admin/pages-error-404.html' 
class PagesRegister(TemplateView):
    template_name="admin/pages-register.html"
class FormsValidation(TemplateView):
    template_name='admin/forms-validation.html'
class UsersProfile(TemplateView):
    template_name='admin/users-profile.html'    
class PagesRegister(TemplateView):
    template_name='admin/pages-register.html'
class PagesError404(TemplateView):
    template_name='admin/pages-error-404.html'      
class TablesData(TemplateView):
    template_name='admin/tables-data.html'
class PagesLogin(TemplateView):
    template_name='admin/pages-login.html'
class ChartsApexchart(TemplateView):
    template_name='admin/charts-apexchart/html'


# class UserRegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'admin/pages-register.html'
#     success_url = reverse_lazy('users:home')  

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)  
#         return redirect(self.success_url)


# class UserLoginView(LoginView):
#     authentication_form = EmailAuthenticationForm
#     template_name = 'admin/pages-login.html'

class RegisterView(FormView):
    template_name = 'admin/pages-register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:home')  

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Use password1 from UserCreationForm
        user.save()

        if user.role == 1:
            Patient.objects.create(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
        # Log the user in immediately
        login(self.request, user)
        return redirect(self.get_success_url())

class LoginView(View):
    def get(self, request):
        return render(request, 'admin/pages-login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if user.role == 1:
                return redirect('users:home')
            elif user.role == 2:
                return redirect('doctor_dashboard')
            elif user.role == 3:
                return redirect('admin_dashboard')
        else:
            return render(request, 'admin/pages-login.html', {'error': 'Invalid credentials'})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RoleRequiredMixin(UserPassesTestMixin):
    role_required = None

    def test_func(self):
        return self.request.user.role == self.role_required


# Patient Views
class PatientDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'patient/dashboard.html'
    context_object_name = 'appointments'
    role_required = 1

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)


class DoctorListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Doctor
    template_name = 'patient/list_doctors.html'
    context_object_name = 'doctors'
    role_required = 1


class BookAppointmentView(LoginRequiredMixin, RoleRequiredMixin, View):
    role_required = 1

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        form = AppointmentForm()
        return render(request, 'patient/book_appointment.html', {'doctor': doctor, 'form': form})

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)
        form = AppointmentForm(request.POST)
        if form.is_valid():
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=form.cleaned_data['appointment_date'],
                reason=form.cleaned_data['reason'],
            )
            return redirect('patient_dashboard')
        return render(request, 'patient/book_appointment.html', {'doctor': doctor, 'form': form})


# Doctor Views
class DoctorDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'doctor/dashboard.html'
    context_object_name = 'appointments'
    role_required = 2

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)


class DoctorAppointmentsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'doctor/appointments.html'
    context_object_name = 'appointments'
    role_required = 2

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)


class UpdateAppointmentView(LoginRequiredMixin, RoleRequiredMixin, View):
    role_required = 2

    def get(self, request, appt_id):
        appointment = get_object_or_404(Appointment, id=appt_id, doctor__user=request.user)
        return render(request, 'doctor/update_appointment.html', {'appointment': appointment})

    def post(self, request, appt_id):
        appointment = get_object_or_404(Appointment, id=appt_id, doctor__user=request.user)
        status = request.POST.get('status')
        if status in ['Completed', 'Cancelled']:
            appointment.status = status
            appointment.save()
        return redirect('doctor_appointments')


# Admin Views
class AdminDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Doctor
    template_name = 'admin/dashboard.html'
    context_object_name = 'doctors'
    role_required = 3


class AddDoctorView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'admin/add_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('admin_dashboard')
    role_required = 3

    def form_valid(self, form):
        user = form.save_user()
        Doctor.objects.create(
            user=user,
            specialty=form.cleaned_data['specialty'],
            phone=form.cleaned_data['phone'],
            availability=form.cleaned_data['availability']
        )
        return super().form_valid(form)
