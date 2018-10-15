from django.db import models
import datetime

from django.db.models import Count ,Sum ,F ,Avg



class Courses(models.Model):
    name_course = models.CharField(max_length=200)
    name_techer = models.CharField(max_length=200)
    phone_nemper = models.CharField(max_length=10, null=True, blank=True)
    nick_name = models.CharField(max_length=200, null=True, blank=True)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    is_show = models.BooleanField(default=True)
    order_show = models.IntegerField(null=True)
    numper_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)

    def conut_student(self):
        from .students import Students
        return Students.objects.filter(course=self ,is_show=True).aggregate(count=Count('id'))['count']

    def __str__(self):
        return self.name_course

class Week(models.Model):
    name = models.CharField(max_length=50)

class Days(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(default=datetime.datetime.now(),null=True, blank=True)
    end_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    course=None

    def __str__(self):
        return str(self.name)

    def date_hijri(self):
        from library.umalqurra.hijri_date import HijriDate
        um = HijriDate(self.start_time)
        return  um.date_hijri()

    def set_course(self,course):
        self.course=course

    def get_course(self):
        return self.course

    def conut_student(self):
        if(self.course==None):
            return 'erorr'
        from .students import Tasks_days
        return str(Tasks_days.objects.filter(days=self,student__course__id=self.course.id).aggregate(count=Count('id'))['count'])

    def conut_presence_student(self):
        try:
            return str(int(self.conut_student())-int(self.conut_truant_student()))
        except:
            return 'erorr'

    def conut_truant_student(self):
        if (self.course == None):
            return 'erorr'
        from .students import Tasks_days
        from django.db.models import Q
        return str(
            Tasks_days.objects.filter(days=self, student__course__id=self.course.id).filter(Q(present=False)|Q(present=None)).aggregate(count=Count('id'))['count'])



    def sum_count_save(self):
        if (self.course == None):
            return 'erorr'
        from .students import Tasks_days
        return str(
            Tasks_days.objects.filter(days=self, student__course__id=self.course.id).aggregate(sum=Sum('count_save'))[
                'sum'])



    def sum_count_link(self):
        if (self.course == None):
            return 'erorr'
        from .students import Tasks_days
        return str(
            Tasks_days.objects.filter(days=self, student__course__id=self.course.id).aggregate(sum=Sum('count_link'))[
                'sum'])



    def sum_count_erorr(self):
        if (self.course == None):
            return 'erorr'
        from .students import Tasks_days
        return str(
            Tasks_days.objects.filter(days=self, student__course__id=self.course.id).aggregate(sum=Sum('count_erorr'))[
                'sum'])

    def sum_count_alirt(self):
        if (self.course == None):
            return 'erorr'
        from .students import Tasks_days
        return str(
            Tasks_days.objects.filter(days=self, student__course__id=self.course.id).aggregate(sum=Sum('count_alirt'))[
                'sum'])
