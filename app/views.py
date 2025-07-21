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
class ComponentsAccordion(TemplateView):
    template_name='admin/components-accordion.html'
class UsersProfile(TemplateView):
    template_name= "admin/users-profile.html"

class FormsValidation(TemplateView):
    template_name='admin/forms-validation.html'
class PagesRegister(TemplateView):
    template_name="admin/pages-register.html"
class PagesError404(TemplateView):
    template_name='admin/pages-error-404.html'      
class TablesData(TemplateView):
    template_name='admin/tables-data.html'
class PagesLogin(TemplateView):
    template_name='admin/pages-login.html'
class ChartsApexchart(TemplateView):
    template_name='admin/charts-apexcharts.html'
class ChartsEharts(TemplateView):
    template_name='admin/charts-echarts.html'
class ComponentsAlerts(TemplateView):
    template_name='admin/components-alerts.html'
class ComponentBreadcrumbs(TemplateView):
    template_name='admin/components-breadcrumbs.html'
class ComponentBadges(TemplateView):
    template_name='admin/components-badges.html'
class ComponentsButtons(TemplateView):
    template_name='admin/components-buttons.html'
class ComponentsCards(TemplateView):
    template_name='admin/components-cards.html'
class ComponentsCarousel(TemplateView):
    template_name='admin/components-carousel.html'
class ComponentsListGroup(TemplateView):
    template_name='admin/components-list-group.html'
class ComponentsModal(TemplateView):
    template_name='admin/components-modal.html'
class ComponentsPagination(TemplateView):
    template_name='admin/components-pagination.html'
class ComponentsProgress(TemplateView):
    template_name='admin/components-progress.html'
class ComponentsSpinners(TemplateView):
    template_name='admin/components-spinners.html'
class ComponentsTabs(TemplateView):
    template_name='admin/components-tabs.html'
class ComponentsTooltips(TemplateView):
    template_name='admin/components-tooltips.html'
class FormsEditors(TemplateView):
    template_name='admin/forms-editors.html'
class FormsElements(TemplateView):
    template_name='admin/forms-elements.html'
class FormsLayouts(TemplateView):
    template_name='admin/forms-layouts.html'
class IconsBootstrap(TemplateView):
    template_name='admin/icons-bootstrap.html'
class IconsBboxicons(TemplateView):
    template_name='admin/icons-boxicons.html'
class IconsRemix(TemplateView):
    template_name='admin/icons-remix.html'
class PagesBlank(TemplateView):
    template_name='admin/pages-blank.html'
class PagesContact(TemplateView):
    template_name='admin/pages-contact.html'
class PagesFaq(TemplateView):
    template_name='admin/pages-faq.html'
class TablesGeneral(TemplateView):
    template_name='admin/tables-general.html'



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
                return redirect(reverse_lazy('users:home'))
            elif user.role == 2:
                return redirect(reverse_lazy('users:doctor_dashboard'))
            elif user.role == 3:
                return redirect(reverse_lazy('users:admin_dashboard'))
        else:
            return render(request, 'admin/pages-login.html', {'error': 'Invalid credentials'})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("users:login"))


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


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'admin/patient/list_doctors.html'
    context_object_name = 'doctors'
    # role_required = (1,2,3)


class BookAppointmentView(LoginRequiredMixin, RoleRequiredMixin, View):
    role_required = 1

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        form = AppointmentForm()
        return render(request, 'admin/patient/book_appointment.html', {'doctor': doctor, 'form': form})

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
            return redirect(reverse_lazy('users:home'))
        return render(request, 'admin/patient/book_appointment.html', {'doctor': doctor, 'form': form})


# Doctor Views
class DoctorDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'admin/index.html'
    context_object_name = 'appointments'
    role_required = 2

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)


class DoctorAppointmentsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'admin/doctor/appointments.html'
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
        return redirect(reverse_lazy('users:doctor_appointments'))


# Admin Views
class AdminDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    print("calleds")
    model = Doctor
    template_name = 'admin/index.html'
    context_object_name = 'doctors'
    role_required = 3


# class AddDoctorView(LoginRequiredMixin, FormView):
#     template_name = 'admin/doctor/add_doctor.html'
#     print("template_name",template_name)
#     form_class = DoctorForm
#     success_url = reverse_lazy('users:list_doctor')
#     role_required = 3

#     def form_valid(self, form):
#         user = form.save_user()
#         Doctor.objects.create(
#             user=user,
#             specialty=form.cleaned_data['specialty'],
#             phone=form.cleaned_data['phone'],
#             availability=form.cleaned_data['availability']
#         )
#         return super().form_valid(form)

class AddDoctorView(LoginRequiredMixin, FormView):
    template_name = 'admin/doctor/add_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('users:list_doctor')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class UpdateDoctorView(LoginRequiredMixin, UpdateView):
#     model = Doctor
#     form_class = DoctorForm
#     template_name = 'admin/doctor/add_doctor.html'  # Reuse the same form
#     success_url = reverse_lazy('users:list_doctor')

#     def get_initial(self):
#         initial = super().get_initial()
#         user = self.object.user
#         initial.update({
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#         })
#         return initial

#     def form_valid(self, form):
#         doctor = form.save(commit=False)
#         user = doctor.user
#         user.first_name = form.cleaned_data['first_name']
#         user.last_name = form.cleaned_data['last_name']
#         user.email = form.cleaned_data['email']
#         user.save()
#         doctor.specialty = form.cleaned_data['specialty']
#         doctor.phone = form.cleaned_data['phone']
#         doctor.availability = form.cleaned_data['availability']
#         doctor.save()
#         return super().form_valid(form)

class UpdateDoctorView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'admin/doctor/add_doctor.html'
    success_url = reverse_lazy('users:list_doctor')

    def get_initial(self):
        initial = super().get_initial()
        user = self.object.user
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        return initial    
class DeleteDoctorView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'admin/doctor/delete_confirm.html'
    success_url = reverse_lazy('users:admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor_name'] = self.object.user.get_full_name()
        return context

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'admin/pages-error-404.html', {
        'error_code': 404,
        'error_message': 'Page Not Found'
    }, status=404)

def custom_500(request):
    return render(request, 'admin/pages-error-404.html', {
        'error_code': 500,
        'error_message': 'Internal Server Error'
    }, status=500)

def custom_403(request, exception):
    return render(request, 'admin/pages-error-404.html', {
        'error_code': 403,
        'error_message': 'Permission Denied'
    }, status=403)

def custom_400(request, exception):
    return render(request, 'admin/pages-error-404.html', {
        'error_code': 400,
        'error_message': 'Bad Request'
    }, status=400)
