from django.contrib import admin
from ramadan.models import Courses, Students, Days, Tasks_days

# Register your models here.
class Days_Admin(admin.ModelAdmin):
    list_display = ['__str__','start_time','end_time']
    class Meta:
        model=Days

class Tasks_days_Admin(admin.ModelAdmin):
    list_display = ['student']
    class Meta:
        model=Tasks_days


class Courses_Admin(admin.ModelAdmin):
    list_display = ['__str__','name_techer','numper_user','password']
    class Meta:
        model=Courses




admin.site.register(Courses,Courses_Admin)
admin.site.register(Students)
admin.site.register(Days,Days_Admin)
admin.site.register(Tasks_days,Tasks_days_Admin)


