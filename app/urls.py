from django.urls import path
from app.views import *
from django.contrib.auth.views import LogoutView
app_name="users"
urlpatterns = [
    path("",Home.as_view(),name="home"),
    path("charts-chartjs",ChartsChartjs.as_view(),name="charts_chartjs"),
    path("charts-echarts",ChartsEharts.as_view(),name="charts_echarts"),
    path("components-accordion",ComponentsAccordion.as_view(),name="components_accordion"),
    path("users-profile/", UsersProfile.as_view(), name="users_profile"),
    # path("tables-data/", TablesData.as_view(), name="tables_data"),
    path("pages-error-404/", PagesError404.as_view(), name="pages_error_404"),
    path("pages-register/",PagesRegister.as_view(), name="pages_register"),
    path("forms-validation/", FormsValidation.as_view(), name="forms_validation"),
    path("users-profile/",UsersProfile.as_view(), name="users_profile"),
    path("pages-register/", PagesRegister.as_view(), name="pages_register"),
    path("pages-error-404/", PagesError404.as_view(), name="pages_error_404"),
    path("tables-data/",TablesData.as_view(), name="tables_data"),
    path("pages-login/", PagesLogin.as_view(), name="pages_login"),
    path("charts-apexchart/",ChartsApexchart.as_view(),name="charts-apexchart"),




    # for AUTHENTICATIN
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    path('patient/dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('patient/doctors/', DoctorListView.as_view(), name='list_doctors'),
    path('patient/book/<int:doctor_id>/', BookAppointmentView.as_view(), name='book_appointment'),

    path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctor/appointments/', DoctorAppointmentsView.as_view(), name='doctor_appointments'),
    path('doctor/appointment/<int:appt_id>/update/', UpdateAppointmentView.as_view(), name='update_appointment'),

    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/add_doctor/', AddDoctorView.as_view(), name='add_doctor'),

]



