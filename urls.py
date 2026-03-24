from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('marks/', include('marks.urls')),
    path('', lambda request: redirect('marks:student_list')),
]