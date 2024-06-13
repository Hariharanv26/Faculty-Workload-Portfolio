from . import views
from django.urls import path


urlpatterns= [
    path('',views.home,name='workload-home'),
    path('login',views.login_view,name='login'),
    path('time/',views.time,name='workload-time'),
    path('academic/',views.academic,name='workload-academic'),
    path('filter',views.filterDetails,name='filter'),
    path('view_work/',views.viewWorkload,name='workload-view'),
    path('get_fac_details',views.get_fac_details,name='get_fac_details'),
    path('update_workload/',views.update_workload,name='workload-update'),
    path('add-course',views.add_courses,name='add-course'),
    path('remove-course',views.remove_courses,name='remove-course'),
    path('assign-course',views.assign_courses,name='assign-course'),
    path('remove-assign-course',views.remove_assign_course,name='remove-assign-course'),
    path('button-chk',views.changeUpdateInfo,name='button-chk'),
    path('department',views.department,name='workload-department'),
    path('assign-dept-duty',views.assignDeptDuty,name='assign-dept-duty'),
    path('remove-dept-duty',views.removeDeptDuty,name='remove-dept-duty')
]