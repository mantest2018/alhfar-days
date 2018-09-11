from django.urls import path, re_path
from ramadan import views


urlpatterns = [

    re_path(r'^$', views.home_page, name='home_page'),
    path('weekNow/',views.weekNow, name='weekNow'),
    path('register/',views.register, name='register'),




    # الخطة
    path('update/',views.update, name='update'),
    path('donload_report/',views.donload_report, name='donload_report'),
    #   path('register/',  views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    #          techer  tasks_weeks
    path('tasks_weeks/<int:week_id>/student/<int:student_id>/', views.tasks_weeks, name='student_tasks'),
    # path('tasks_weeks/<int:student_id>/<int:week_id>', views.tasks_weeks, name='student_tasks'),


    path('students/', views.students, name='students_course'),
    path('students/<int:week_id>/', views.students, name='report_course'),
    # يوجد خلل
    path('report/<int:student_id>/', views.report, name='report_student'),
    path('all_week/', views.all_week, name='report_student'),


    # control  add and remove student
    path('remove/<int:student_id>/', views.remove, name='remove'),


    path('report/', views.report, name='report'),


    path('report_day/tasks/', views.tasks_report_day, name='report'),
    path('report_day/tasks/<int:day_id>/', views.tasks_report_day, name='report'),

    path('report/', views.report, name='report'),
    path('report_view/', views.report_view, name='report_view'),
    path('report_view/<int:weekR>/', views.report_view, name='report_view'),

]
