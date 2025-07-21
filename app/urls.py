from django.urls import path
from app.views import *
# from django.contrib.auth.views import LogoutView
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
    path("charts-apexcharts/",ChartsApexchart.as_view(),name="charts_apexcharts"),
    path("components-alerts/", ComponentsAlerts.as_view(), name="components_alerts"),
    path("components-breadcrumbs/", ComponentBreadcrumbs.as_view(), name="components-breadcrumbs"),
    path("components-badges/", ComponentBadges.as_view(), name="components-badges"),
    path("components-buttons/",ComponentsButtons .as_view(), name="components-buttons"),
    path("components-cards/", ComponentsCards.as_view(), name="components-cards"),
    path("components-carousel/", ComponentsCarousel.as_view(), name="components-carousel"),
    path("components-list-group/", ComponentsListGroup.as_view(), name="components-list-group"),
    path("components-modal/",ComponentsModal .as_view(), name="components-modal"),
    path("components-pagination/",ComponentsPagination.as_view(), name="components-pagination"),
    path("components-progress/", ComponentsProgress.as_view(), name="components-progress"),
    path("components-spinners/", ComponentsSpinners.as_view(), name="components-spinners"),
    path("components-tabs/", ComponentsTabs.as_view(), name="components-tabs"),
    path("components-tooltips/", ComponentsTooltips.as_view(), name="components-tooltips"),
    path("forms-editors/", FormsEditors.as_view(), name="forms-editors"),
    path("forms-elements/",FormsElements .as_view(), name="forms-elements"),
    path("forms-layouts/",FormsLayouts .as_view(), name="forms-layouts"),
    path("icons-bootstrap/", IconsBootstrap.as_view(), name="icons-bootstrap"),
    path("icons-boxicons/", IconsBboxicons.as_view(), name="icons-boxicons"),
    path("icons-remix/",IconsRemix .as_view(), name="icons-remix"),
    path("pages-blank/", PagesBlank.as_view(), name="pages-blank"),
    path("pages-contact/", PagesContact.as_view(), name="pages-contact"),
    path("pages-faq/", PagesFaq.as_view(), name="pages-faq"),
    path("tables-general/", TablesGeneral.as_view(), name="tables-general"),

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

    path('admins/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admins/add_doctor/', AddDoctorView.as_view(), name='add_doctor'),
    path('admins/doctor/', DoctorListView.as_view(), name='list_doctor'),
    path('admins/edit_doctor/<int:pk>/', UpdateDoctorView.as_view(), name='edit_doctor'),
    path('admins/delete_doctor/<int:pk>/', DeleteDoctorView.as_view(), name='delete_doctor'),

]



