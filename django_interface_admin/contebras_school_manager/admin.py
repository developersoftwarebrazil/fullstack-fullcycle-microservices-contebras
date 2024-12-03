from django.contrib import admin

from contebras_school_manager.models import Course, Student,Classroom



# Register your models here.
class CourseAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')

class StudantAdmin(admin.ModelAdmin):
  list_display = ('name', 'email')

class ClassroomAdmin(admin.ModelAdmin):
  list_display = ('name', 'course')
  filter_horizontal = ('student')
  
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Classroom)
# admin.site.register(RegistrationClassroom)