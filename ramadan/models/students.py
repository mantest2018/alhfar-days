from .models import *
from django.db import models
from django.utils import timezone
from django.db.models import Q


def day_now():
    t = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    return Days.objects.filter(Q(start_time__lte=t) | Q(id=1)).latest('id').id


class Students(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    name_student = models.CharField(max_length=200)
    phone_nemper = models.CharField(max_length=10)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    numper_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.name_student

    # تحديث درجات الطالب عند تغيير مساره
    def save(self, *args, **kwargs):
        super(Students, self).save(*args, **kwargs)
        if not self.is_show:
            for item in Days.objects.filter(id__gt=day_now()):
                try:
                    report = Tasks_days.objects.get(student=self, days=item)
                except:
                    continue
        else:
            for item in Days.objects.filter(id__gte=day_now()):
                try:
                    Tasks_days.objects.get(student=self, days=item)
                except:
                    report = Tasks_days(student=self, days=item)
                    report.save()
        report = Tasks_days.objects.filter(student=self)
        for repo in report:
            repo.save()


# Sup المفترض Im التنفيذ
class Tasks_days(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    days = models.ForeignKey(Days, on_delete=models.CASCADE)

    present = models.BooleanField(default=True)

    save_from = models.CharField(max_length=50, null=True, blank=True)
    save_to = models.CharField(max_length=50, null=True, blank=True)

    link_from = models.CharField(max_length=50, null=True, blank=True)
    link_to = models.CharField(max_length=50, null=True, blank=True)

    count_save = models.FloatField(default=0, null=True, blank=True)
    count_erorr = models.IntegerField(default=0)
    count_alirt = models.IntegerField(default=0)

    count_link = models.FloatField(default=0, null=True, blank=True)


