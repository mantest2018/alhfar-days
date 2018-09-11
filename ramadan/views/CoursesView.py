from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from ..models import Weeks ,Tasks_weeks ,Courses
from .views import is_login,week_now


def report_students_Courses(request, week_now=week_now()):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] != 'techer':
            return HttpResponseRedirect('/')
        day = Weeks.objects.get(pk=week_now).name_day
        latest_list = Tasks_weeks.objects.filter(student__course=request.session['member_id'],
                                                 weeks__id=week_now)
        course = Courses.objects.get(pk=request.session['member_id'])
        context = {'latest_list': latest_list, 'course': course, 'week_now': week_now, 'day': day}
    except(Courses.DoesNotExist, Tasks_weeks.DoesNotExist):
        return HttpResponse('يوجد خطأ تواصل مع مسئول البرنامج')
    return render(request, 'Courses/report_students_Courses.html', context)
