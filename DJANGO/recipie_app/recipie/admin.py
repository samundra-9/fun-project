from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Recipie)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SubjectMarks)

