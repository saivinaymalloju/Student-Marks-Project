# Django Student Marks Manager

> A beginner-friendly Django CRUD web application to manage student marks — with auto-calculated totals, percentages, and grades.

---

## Table of Contents

- [What is This Project?](#what-is-this-project)
- [What is CRUD?](#what-is-crud)
- [Technologies Used](#technologies-used)
- [Project Folder Structure](#project-folder-structure)
- [Step 1 — settings.py](#step-1--settingspy)
- [Step 2 — models.py](#step-2--modelspy--the-database-table)
- [Step 3 — forms.py](#step-3--formspy--the-form)
- [Step 4 — views.py](#step-4--viewspy--the-logic)
- [Step 5 — urls.py](#step-5--urlspy--url-routing)
- [Step 6 — Templates](#step-6--templates)
- [Step 7 — admin.py](#step-7--adminpy--admin-panel)
- [Complete Request Flow](#complete-request-flow)
- [All URLs Summary](#all-urls-summary)
- [Key Concepts Summary](#key-concepts-summary)
- [How to Run the Project](#how-to-run-the-project)
- [Common Error and Fix](#common-error-and-fix)

---

## What is This Project?

This is a **Django CRUD Web Application** that manages student marks. A teacher or admin can:

- **Add** a new student with subject marks
- **View** all students in a table with stats
- **View Detail** of a single student
- **Edit** student information and marks
- **Delete** a student with a confirmation page
- **Auto-calculate** Total Marks, Percentage, and Grade

---

## What is CRUD?

CRUD is the foundation of almost every web application:

| Letter | Meaning | In This Project | URL |
|--------|---------|----------------|-----|
| **C** | Create | Add new student | `/marks/add/` |
| **R** | Read | View list / detail | `/marks/` and `/marks/1/` |
| **U** | Update | Edit student | `/marks/1/edit/` |
| **D** | Delete | Remove student | `/marks/1/delete/` |

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11.9 | Programming language |
| Django | 4.2 | Web framework |
| SQLite | Built-in | Database |
| Bootstrap | 5.3 | CSS styling |
| HTML/CSS | — | Frontend templates |

---

## Project Folder Structure

```
student_marks_project/
│
├── manage.py                        ← Django command tool
│
├── student_marks_project/           ← Project config folder
│   ├── __init__.py                  ← Makes it a Python package
│   ├── settings.py                  ← All configurations
│   ├── urls.py                      ← Main URL router
│   └── wsgi.py                      ← Deployment entry point
│
└── marks/                           ← Our app (all logic here)
    ├── __init__.py                  ← Makes it a Python package
    ├── models.py                    ← Database structure (Student table)
    ├── forms.py                     ← Add/Edit form with validation
    ├── views.py                     ← All page logic (CRUD functions)
    ├── urls.py                      ← URL routes for marks app
    ├── admin.py                     ← Admin panel config
    └── templates/
        └── marks/
            ├── base.html            ← Master layout
            ├── student_list.html    ← All students + stats
            ├── student_form.html    ← Add / Edit form
            ├── student_detail.html  ← Single student detail
            └── confirm_delete.html  ← Delete confirmation page
```

---

## 4Step 1 — `settings.py`

The **configuration file** of the entire project.

### INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',     # admin panel at /admin/
    'django.contrib.auth',      # user authentication system
    'django.contrib.sessions',  # session management
    'marks',                    # OUR app registered here
]
```

### DATABASES

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # all data saved in this file
    }
}
```

> SQLite is a **file-based database** — no setup needed, perfect for learning projects.

---

## Step 2 — `models.py` — The Database Table

The **Model** defines what data we store in the database.

```python
class Student(models.Model):
    name      = models.CharField(max_length=100)
    roll_no   = models.CharField(max_length=20, unique=True)
    email     = models.EmailField(unique=True)

    maths     = models.IntegerField(default=0)
    science   = models.IntegerField(default=0)
    english   = models.IntegerField(default=0)
    history   = models.IntegerField(default=0)
    computer  = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
```

### Model Methods — Auto Calculations

```python
def total_marks(self):
    return self.maths + self.science + self.english + self.history + self.computer

def percentage(self):
    return round((self.total_marks() / 500) * 100, 2)

def grade(self):
    p = self.percentage()
    if p >= 90:   return 'A+'
    elif p >= 80: return 'A'
    elif p >= 70: return 'B+'
    elif p >= 60: return 'B'
    elif p >= 50: return 'C'
    else:         return 'F'
```

### Grade Logic Table

| Percentage | Grade | Result |
|----------- |-------|--------|
| 90% – 100% | A+    | Pass   |
| 80% – 89%  | A     | Pass   |
| 70% – 79%  | B+    | Pass   |
| 60% – 69%  | B     | Pass   |
| 50% – 59%  | C     | Pass   |
| Below 50%  | F     | Fail   |

### Migration Commands

```bash
python manage.py makemigrations   # reads models.py → creates migration file
python manage.py migrate          # applies migration → creates DB table
```

---

## Step 3 — `forms.py` — The Form

The form handles **user input** and **validation** for adding and editing students.

```python
class StudentForm(forms.ModelForm):

    maths = forms.IntegerField(
        min_value=0, max_value=100,   # only 0-100 allowed
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model  = Student
        fields = ['name', 'roll_no', 'email',
                  'maths', 'science', 'english', 'history', 'computer']
```

### What is ModelForm?

```
Normal Form  →  you write every field manually
ModelForm    →  Django reads your Model and builds the form automatically
```

### Validation Flow

```
User enters maths = 150
        ↓
max_value=100 check fails
        ↓
Error: "Ensure this value is less than or equal to 100"
        ↓
Form NOT saved 

User enters maths = 85
        ↓
Validation passes 
        ↓
Saved to database
```

---

## Step 4 — `views.py` — The Logic

Each view is a **Python function** that handles one page or action.

### student_list — View All Students

```python
def student_list(request):
    students = Student.objects.all()        # fetch ALL students from DB
    total_students = students.count()

    avg_percentage = round(
        sum(s.percentage() for s in students) / total_students, 2
    )
    top_student = max(students, key=lambda s: s.percentage())
```

### student_add — Add New Student

```python
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()                     # save to database
            return redirect('marks:student_list')
    else:
        form = StudentForm()                # show empty form
```

### student_edit — Edit Existing Student

```python
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        #                               ↑ instance= means UPDATE not CREATE
        if form.is_valid():
            form.save()
    else:
        form = StudentForm(instance=student)   # pre-fill with existing data
```

### Add vs Edit Difference

| | Add | Edit |
|--|-----|------|
| Form | `StudentForm(request.POST)` | `StudentForm(request.POST, instance=student)` |
| DB Action | Creates new record | Updates existing record |
| Form pre-filled | No (empty) | Yes (existing data) |

### student_delete — Delete Student

```python
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()                    # remove from database
        return redirect('marks:student_list')

    return render(request, 'marks/confirm_delete.html', {'student': student})
```

### Delete Flow

```
User clicks Delete
        ↓
GET → Show "Are you sure?" confirmation page
        ↓
User clicks "Yes, Delete"
        ↓
POST → student.delete() → removed from DB
        ↓
Redirect to student list 
```

### What is get_object_or_404?

```python
student = get_object_or_404(Student, pk=pk)

# Same as writing:
try:
    student = Student.objects.get(pk=pk)
except Student.DoesNotExist:
    raise Http404   # shows proper 404 page
```

> This is a **safety shortcut** — if someone types a wrong ID in the URL, they get a proper 404 page instead of a server crash.

---

## Step 5 — `urls.py` — URL Routing

### Main `urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('marks/', include('marks.urls')),
    path('', lambda request: redirect('marks:student_list')),
]
```

### `marks/urls.py`

```python
app_name = 'marks'

urlpatterns = [
    path('',                 views.student_list,   name='student_list'),
    path('add/',             views.student_add,    name='student_add'),
    path('<int:pk>/',        views.student_detail, name='student_detail'),
    path('<int:pk>/edit/',   views.student_edit,   name='student_edit'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
]
```

### What is `<int:pk>`?

```
URL: /marks/3/edit/
               ↑
               pk = 3  (primary key / ID of the student)

Django captures this number and passes it to the view:
def student_edit(request, pk):   ← pk = 3 here
```

---

## 🔷 Step 6 — Templates

### Template Inheritance

```
base.html              (parent — navbar, flash messages)
        ↑
    extends
        ↑
student_list.html      (child — fills block content)
student_form.html      (child — fills block content)
student_detail.html    (child — fills block content)
confirm_delete.html    (child — fills block content)
```

### base.html Layout

```
┌──────────────────────────────────────┐
│      Student Marks Manager   + Add   │  ← Navbar (same on all pages)
├──────────────────────────────────────┤
│     Student added successfully!      │  ← Flash messages
├──────────────────────────────────────┤
│                                      │
│        {% block content %}           │  ← Each page fills this
│                                      │
└──────────────────────────────────────┘
```

---

##  Step 7 — `admin.py` — Admin Panel

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['roll_no', 'name', 'email', 'total_marks', 'percentage', 'grade']
    search_fields = ['name', 'roll_no', 'email']
```

> Visit `http://127.0.0.1:8000/admin/` after creating a superuser to manage all student data from Django's built-in admin interface.

---

##  Complete Request Flow

```
Browser types /marks/add/
        ↓
Main urls.py → sees "marks/" → passes to marks/urls.py
        ↓
marks/urls.py → matches "add/" → calls student_add view
        ↓
student_add view:
    GET?  → create empty StudentForm → render student_form.html
    POST? → validate form → save to DB → redirect to list
        ↓
Template renders and sends HTML back to browser
```

---

##  All URLs Summary

| URL               | View Function | Action |
|-------------------|--------------|--------|
| `/`               | — | Redirect to student list |
| `/marks/` | `student_list` | Show all students + stats |
| `/marks/add/` | `student_add` | Add new student |
| `/marks/1/` | `student_detail` | View student with ID = 1 |
| `/marks/1/edit/` | `student_edit` | Edit student with ID = 1 |
| `/marks/1/delete/` | `student_delete` | Delete student with ID = 1 |
| `/admin/` | Django Admin | Manage all data |

---

## 🔷 Key Concepts Summary

|     Concept         |        What it does         |       Where used              |
|---------------------|-----------------------------|-------------------------------|
| `models.Model`      | Defines DB table structure  | `models.py`                   |
| `ModelForm`         | Auto-builds form from model | `forms.py`                    |
| `objects.all()`     | Fetch all records from DB   | `student_list` view           |
| `get_object_or_404` | Fetch one record safely     | edit, delete, detail views    |
| `form.save()`       | Save form data to DB        | `student_add`, `student_edit` |
| `instance=student`  | Pre-fill form for editing   | `student_edit` view           |
| `student.delete()`  | Remove record from DB       | `student_delete` view         |
| `<int:pk>`          | Capture ID from URL         | All detail/edit/delete URLs   |
| `@admin.register`   | Show model in admin panel   | `admin.py`                    |
| `makemigrations`    | Create migration file       | Terminal command              |
| `migrate`           | Apply changes to DB         | Terminal command              |

---

## How to Run the Project

### 1. Install Django

```bash
pip install django==4.2
```

### 2. Create Project and App

```bash
django-admin startproject student_marks_project
cd student_marks_project
python manage.py startapp marks
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

### 6. Open in Browser

```
http://127.0.0.1:8000/
```

---

## Common Error and Fix

### `TemplateSyntaxError: Invalid filter: 'split'`

**Cause:** Django templates do not have a built-in `split` filter.

**Broken code in `student_form.html`:**

```html
{% for subject in 'maths science english history computer'|split:' ' %}
{% endfor %}
```

**Fix:** Remove that loop entirely and list each subject field directly in the template. Django does not support `split` as a template filter out of the box.

---

> Once you understand this project, you have a strong foundation in Django CRUD — the core of almost every real-world web application!
