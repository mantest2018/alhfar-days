from django.template import RequestContext
from django.db.models import Sum

from ramadan.form import Students_Form
from .views import *
from django.template.loader import render_to_string


def home_page(request):
    if is_login(request):
        if request.session['user_type'] == 'techer':
            return students(request)
    return report(request)


def report(request):
    last_week = Days.objects.filter(id__lt=day_now()).latest('id')
    tasks = Tasks_days.objects.filter(days__id=last_week.id)
    context = dict(
        save_pages = tasks.aggregate(sum=Sum('count_save'))['sum'],
        link_pages = tasks.aggregate(sum=Sum('count_link'))['sum'],
        conut_student=tasks.filter(student__course__is_show=True).aggregate(count=Count('id'))['count'],
        conut_presence=tasks.exclude(Q(present=False) | Q(present=None)).aggregate(count=Count('id'))['count'],
        last_day=last_week,
        report="report_view/",
    )
    csrfContext = RequestContext(request)
    return render(request, 'index.html', context, csrfContext)



def weekNow(request):
    last_week = Days.objects.filter(id__lte=day_now()).latest('id')
    tasks = Tasks_days.objects.filter(days__id=last_week.id)
    context = dict(
        save_pages=tasks.aggregate(sum=Sum('count_save'))['sum'],
        link_pages=tasks.aggregate(sum=Sum('count_link'))['sum'],
        conut_student=tasks.filter(student__course__is_show=True).aggregate(count=Count('id'))['count'],
        conut_presence=tasks.exclude(Q(present=False) | Q(present=None)).aggregate(count=Count('id'))['count'],
        last_day=last_week,
        report="report_view/"+str(last_week.id)+"/",
    )
    csrfContext = RequestContext(request)
    return render(request, 'index.html', context, csrfContext)

is_update = False

def report_view(request,weekR=''):
    if request.GET:
         return HttpResponseRedirect('/')
    global is_update
    if weekR=='':
        is_up=(is_update == day_now())
        weekR = day_past()
        path = 'cache/' + 'index.html'
    else:
        is_up=False
        path = 'cache/index' + str(weekR) + '.html'
        weekR = Days.objects.get( id=weekR)
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if is_up:
        try:
            f = open(os.path.join(BASE_DIR, path), 'r+')
            content = f.read()
        except IOError:
            content = 'أنتظر قليلاً ثم حدث الصفحة'
    else:
        # is_update = day_now()

        try:

            latest_list=[]

            course = Courses.objects.filter(is_show=True)
            for item in course:
                week = Days.objects.get(id=weekR.id)
                week.set_course(item)
                latest_list.append(week)

        except Days.DoesNotExist:
            raise Http404("Days does not exist")


        context = dict(
            latest_list=latest_list,
            week=weekR
        )
        content = render_to_string('report_view.html', context)
        if content is not None:
            f = open(os.path.join(BASE_DIR, path ), 'w+')
            f.write(content)
            f.close()

    return HttpResponse(content)


def donload_report(request):
    import csv
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response, delimiter=';')

    writer.writerow(['الأسم', 'المسار', 'درجة الإختبار الأول', 'درجة الإختبار الثاني', 'الدرجة', 'المستوى العام'])
    for item in Students.objects.filter(is_show=True):
        item.save()
        writer.writerow([item.name_student, item.tracks, item.test1, item.test1, item.ratio(), item.ratio_all()])

    return response


def repair(request):
    return render(request, 'repair.html')


#   Under construction start

def register(request):

    if not is_login(request):
        return HttpResponseRedirect('/')
    try:
        if request.session['user_type'] == 'student':
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            is_save = ''
            if "POST" == request.method:
                student = Students(course_id=request.session['member_id'],)
                fotmedit = Students_Form(request.POST or None, instance=student)
                student.name_student=fotmedit['name_student'].value()
                student.save(new=fotmedit['day'].value())
                # student.save()
                is_save = 'تم حفظ البيانات'
            else:
                fotmedit = Students_Form(request.POST or None)

            context = {'fotmedit': fotmedit,  'is_save': is_save}
            return render(request, 'register.html', context)

    except(Courses.DoesNotExist, Students.DoesNotExist):
        raise Http404("Courses does not exist")

    return Http404("Courses does not exist")
