
from django.contrib import admin
from django.urls import path
from users import views
from management import views as mviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new_user/',views.newuser.as_view()),
    path('gettoken/',views.gettoken.as_view()),
    #path('refreshtoken/',views.refreshtoken.as_view()),
    path('company_register/',views.company_register.as_view()),
    path('company_profile/',views.company_pofile.as_view()),
    path('employer_register/<int:pk>/',views.employer_register.as_view()),
    path('employer_register/',views.employer_register.as_view()),
     path('employer_id/',views.employer_id.as_view()),
    path('employer_profile/',views.employer_profiles.as_view()),
    path('employer_profile/<int:pk>/',views.employer_profiles.as_view()),
    path('projects/<int:pk>/',mviews.projects.as_view()),
    path('projects/',mviews.projects.as_view()),
    path('leaves/',mviews.leaves.as_view()),
    path('leaves/<int:pk>/',mviews.leaves.as_view()),
    path('leave_detail/',mviews.leave_detail.as_view()),
    path('salary/<int:pk>/',mviews.salary.as_view()),
    path('salary/',mviews.salary.as_view()),
    path('salary_detail/',mviews.salary_detail.as_view()),
    path('departments/',mviews.all_departments.as_view()),
    path('add_department/',mviews.add_department.as_view()),
    path('add_department/<int:pk>/',mviews.add_department.as_view()),
    path('attendance/',mviews.attendance.as_view()),
    path('attendance/<int:pk>/',mviews.attendance.as_view()),
    path('my_attendance/',mviews.my_attendance.as_view()),
     path('dashboard/',views.dashboard.as_view()),
    path('forget_password/',views.forget_password.as_view()),
    path('otp/',views.otp.as_view()),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
