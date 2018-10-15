from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from ..models import Days ,Tasks_days ,Courses
from .views import is_login,day_now


def report_students_Courses(request, day_now=day_now()):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] != 'techer':
            return HttpResponseRedirect('/')
        day = Days.objects.get(pk=day_now).name_day
        latest_list = Tasks_days.objects.filter(student__course=request.session['member_id'],
                                                 days__id=day_now)
        course = Courses.objects.get(pk=request.session['member_id'])
        context = {'latest_list': latest_list, 'course': course, 'day_now': day_now, 'day': day}
    except(Courses.DoesNotExist, Tasks_days.DoesNotExist):
        return HttpResponse('يوجد خطأ تواصل مع مسئول البرنامج')
    return render(request, 'Courses/report_students_Courses.html', context)
