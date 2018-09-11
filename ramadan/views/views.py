from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ..models import Students, Courses, Tasks_weeks, Weeks
from django.http import Http404
from ramadan.form import Tasks_weeks_Form
from django.utils import timezone
import datetime
from django.db.models import Q


# Create your views here.

def week_now():
    t = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    return Weeks.objects.filter(Q(start_time__lte=t) | Q(id=1)).latest('id').id

def week_past():
    return Weeks.objects.filter(id__lt=week_now()).latest('id')

def login(request):
    if "POST" == request.method:
        try:
            if request.POST['user_type'] == 'techer':
                m = Courses.objects.get(numper_user=request.POST['id_user'])
                if m.password == request.POST.get("password", ""):
                    request.session['user_type'] = request.POST['user_type']
                    request.session['member_id'] = m.id
                    request.session.set_test_cookie()
                    return HttpResponseRedirect('/')
        except(Courses.DoesNotExist, Students.DoesNotExist):
            erorr_user = 'أسم المستخدم أو كلمة المرور غير صحيحة'
            context = {'erorr_user': erorr_user}
            return render(request, 'login.html', context)
    if request.session.test_cookie_worked():
        return students(request, request.session['member_id'])
    from django import forms
    class FooMultipleChoiceForm(forms.Form):
        id_user = forms.ModelChoiceField(queryset=Courses.objects.all())
        def __init__(self, *args, **kwargs):
            super(FooMultipleChoiceForm, self).__init__(*args, **kwargs)
            self.fields['id_user'].widget.attrs.update({'class': 'form-control input-lg'})

    context = dict(
        courses=FooMultipleChoiceForm(),
    )
    return render(request, 'login.html',context)


def is_login(request):
    return request.session.test_cookie_worked() and "member_id" in request.session

def is_admin(request):
    if is_login(request) :
     return request.session['user_type'] == 'techer'
    return False




def logout(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    if "member_id" in request.session:
        del request.session['member_id']
    if "user_type" in request.session:
        del request.session['user_type']
    return HttpResponseRedirect('/')


def update(request):
    for item in Students.objects.all():
        item.save()
    return HttpResponse("تم")




def students(request, week_id=None):

    if is_login(request):
        if week_id==None:
            week_id = week_now()
        if request.session['user_type'] == 'techer':
            week = Weeks.objects.get(pk=week_id)

            if "POST" == request.method:
                try:
                    report = Tasks_weeks.objects.get(student__id=request.POST['student_id'], student__course__id=request.session['member_id'], weeks__id=week_id)
                    fotmedit = Tasks_weeks_Form(request.POST or None, instance=report)
                    fotmedit.save()
                except:
                    print("erorr")
            latest_list = []
            for tasks_weeks in Tasks_weeks.objects.filter(student__course__id=request.session['member_id'], weeks__id=week_id):
                form = Tasks_weeks_Form(instance=tasks_weeks)
                latest_list.append(form)
            course = Courses.objects.get(pk=request.session['member_id'])
            return render(request, 'Students.html',
                          {'latest_list': latest_list,'course': course, 'week_id': week_id, 'week': week})
        if request.session['user_type'] == 'student':
            return HttpResponseRedirect('/')
    return render(request, 'login.html')


def tasks_report_day(request, week_id=None):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] != 'techer':
            return HttpResponseRedirect('/')
        if week_id==None:
            week_id = week_now()
        day = Weeks.objects.get(pk=week_id).name_day
        latest_list = Tasks_weeks.objects.filter(student__course=request.session['member_id'], student__is_show=True,
                                                 Weeks__id=week_id)
        course = Courses.objects.get(pk=request.session['member_id'])
        context = {'latest_list': latest_list, 'course': course, 'week_id': week_id, 'day': day}
    except(Courses.DoesNotExist, Tasks_weeks.DoesNotExist):
        raise Http404("Courses does not exist")
    return render(request, 'tasks_report_day.html', context)


def all_week(request):
    if is_login(request):
        if request.session['user_type'] == 'student':
            return Tasks_weeks(request, week_now(), request.session['member_id'])
        if request.session['user_type'] == 'techer':
            course = Courses.objects.get(pk=request.session['member_id'])
            try:
                latest_list = Weeks.objects.all().filter(id__lte=week_now()).order_by('pk')

                for item in latest_list:
                    item.set_course(course)
            except Weeks.DoesNotExist:
                raise Http404("Weeks does not exist")

            return render(request, 'AllWeek.html', {'latest_list': latest_list, 'course': course})
    return login(request)


def tasks_objects():
    return Tasks_weeks.objects.filter(Weeks__id__lte=week_now())




def tasks_weeks(request, week_id=None, student_id=''):

    if student_id == '':
        if request.session['user_type'] == 'student':
            student_id = request.session['member_id']
        else:
            return HttpResponseRedirect('/')

    if not is_login(request):
        return HttpResponseRedirect('/')
    if week_id == None:
        week_id = week_now()
    try:
        if request.session['user_type'] == 'student':
            if student_id == request.session['member_id']:
                s = Students.objects.get(pk=request.session['member_id'])
                course_id = s.course.id
        if request.session['user_type'] == 'techer':
            s = Students.objects.get(pk=student_id)
            if s.course.id == request.session['member_id']:
                course_id = request.session['member_id']
        report = Tasks_weeks.objects.get(student__id=student_id, student__course=course_id, weeks__id=week_id)
        is_save = ''
        fotmedit = Tasks_weeks_Form(request.POST or None, instance=report)

        if "POST" == request.method:
            fotmedit.save()
            is_save = 'تم حفظ البيانات'

        context = {'fotmedit': fotmedit, 'report': report, 'is_save': is_save}
    except(Courses.DoesNotExist, Students.DoesNotExist):
        raise Http404("Courses does not exist")
    except(Tasks_weeks.DoesNotExist):
        Student = Students.objects.get(pk=student_id)
        day = Weeks.objects.get(pk=week_id)
        report = Tasks_weeks(student=Student, Weeks=day)
        report.save()
        fotmedit = Tasks_weeks_Form(instance=report)
        context = {'fotmedit': fotmedit, 'report': report}
    return render(request, 'Input_page.html', context)


def chick_student_all_days(student_id):
    Weeeks = Weeks.objects.all()
    for Week in Weeeks:
        try:
            Tasks_weeks.objects.get(student=student_id, Weeks=Week)
        except Tasks_weeks.DoesNotExist:
            Student = Students.objects.get(pk=student_id)
            report = Tasks_weeks(student=Student, Weeks=Week)
            report.save()

 # control  add and remove student

def remove(request, student_id):
    if not is_admin(request):
        return HttpResponse("Nothing")
    if "POST" == request.method:
        try:
            s = Students.objects.get(pk=student_id)
            if s.course.id == request.session['member_id']:
                s.is_show=False
                s.save()
                return HttpResponse("Done")
            else:
                return HttpResponse("Nothing")

        except:
            return HttpResponse("erorr")
    else:
        return HttpResponse("Not found page")
