from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['roll_no', 'name', 'email', 'total_marks', 'percentage', 'grade']
    search_fields = ['name', 'roll_no', 'email']