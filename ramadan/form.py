from django import forms

from .models import Courses, Tasks_days


class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name_course', 'phone_nemper']


class Tasks_days_Form(forms.ModelForm):
    present = forms.BooleanField(label='الحضور',required=False)
    save_from =forms.CharField(label='الحفظ من', required=False)
    save_to = forms.CharField(label='الحفظ إلى', required=False)
    link_from = forms.CharField(label='المراجعة من', required=False)
    link_to =  forms.CharField(label='المراجعة إلى', required=False)
    count_save =forms.FloatField(label='عدد أوجه الحفظ', required=False, min_value=0, max_value=100)
    count_erorr = forms.IntegerField(label='الأخطاء واللحون', required=False, min_value=0, max_value=100)
    count_alirt = forms.IntegerField(label='التنبيهات', required=False, min_value=0, max_value=100)
    count_link =forms.FloatField(label='عدد أوجه المراجعة', required=False, min_value=0, max_value=100)


    class Meta:
        model = Tasks_days
        fields = [ 'present', 'save_from', 'save_to', 'link_from', 'link_to',
                  'count_save', 'count_erorr', 'count_alirt', 'count_link']

class Students_Form(forms.ModelForm):
    name_student =forms.CharField(label='اسم الطالب', required=False)

    class Meta:
        model = Tasks_days
        fields = [ 'name_student']