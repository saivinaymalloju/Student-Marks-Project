from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm


# List all students
def student_list(request):
    students = Student.objects.all()
    total_students = students.count()

    # Simple stats
    if total_students > 0:
        avg_percentage = round(
            sum(s.percentage() for s in students) / total_students, 2
        )
        top_student = max(students, key=lambda s: s.percentage())
    else:
        avg_percentage = 0
        top_student = None

    context = {
        'students': students,
        'total_students': total_students,
        'avg_percentage': avg_percentage,
        'top_student': top_student,
        'bottom_student': min(students, key=lambda s: s.percentage()) if students else None
    }
    return render(request, 'marks/student_list.html', context)


# View single student detail
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'marks/student_detail.html', {'student': student})


# Add new student
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'✅ Student "{student.name}" added successfully!')
            return redirect('marks:student_list')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = StudentForm()

    return render(request, 'marks/student_form.html', {
        'form': form,
        'title': 'Add Student',
        'button': 'Add Student'
    })


# Edit existing student
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Student "{student.name}" updated successfully!')
            return redirect('marks:student_list')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'marks/student_form.html', {
        'form': form,
        'title': 'Edit Student',
        'button': 'Update Student',
        'student': student
    })


# Delete student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'🗑️ Student "{name}" deleted successfully!')
        return redirect('marks:student_list')

    return render(request, 'marks/confirm_delete.html', {'student': student})
