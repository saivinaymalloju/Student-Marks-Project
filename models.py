from django.db import models


class Student(models.Model):

    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'),
        ('B', 'B'),   ('C', 'C'), ('D', 'D'), ('F', 'Fail'),
    ]

    name      = models.CharField(max_length=100)
    roll_no   = models.CharField(max_length=20, unique=True)
    email     = models.EmailField(unique=True)

    # Subject Marks (out of 100)
    maths     = models.IntegerField(default=0)
    science   = models.IntegerField(default=0)
    english   = models.IntegerField(default=0)
    history   = models.IntegerField(default=0)
    computer  = models.IntegerField(default=0)
    biology  = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_marks(self):
        return self.maths + self.science + self.english + self.history + self.computer + self.biology   

    def percentage(self):
        return round((self.total_marks() / 600) * 100, 2)

    def grade(self):
        p = self.percentage()
        if p >= 90:   return 'A+'
        elif p >= 80: return 'A'
        elif p >= 70: return 'B+'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else:         return 'F'

    def grade_color(self):
        colors = {
            'A+': 'success',
            'A':  'success',
            'B+': 'primary',
            'B':  'info',
            'C':  'warning',
            'D':  'secondary',
            'F':  'danger',
        }
        return colors.get(self.grade(), 'secondary')

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

    class Meta:
        ordering = ['roll_no']
        