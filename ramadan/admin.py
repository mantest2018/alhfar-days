from django.contrib import admin
from ramadan.models import Courses, Students, Weeks, Tasks_weeks

# Register your models here.
class Weeks_Admin(admin.ModelAdmin):
    list_display = ['__str__','start_time','end_time']
    class Meta:
        model=Weeks

class Tasks_weeks_Admin(admin.ModelAdmin):
    list_display = ['student']
    class Meta:
        model=Tasks_weeks


class Courses_Admin(admin.ModelAdmin):
    list_display = ['__str__','name_techer','numper_user','password']
    class Meta:
        model=Courses




admin.site.register(Courses,Courses_Admin)
admin.site.register(Students)
admin.site.register(Weeks,Weeks_Admin)
admin.site.register(Tasks_weeks,Tasks_weeks_Admin)


