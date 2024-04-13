from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
class Book(models.Model):
    title = models.CharField(max_length=200)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title
class Student(models.Model):
    name = models.CharField(max_length=100)
    borrowed_books = models.ManyToManyField(Book, through='Loan')

    def __str__(self):
        return self.name
class UserProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
        ('anonymous', 'Anonymous'),  # Technically not stored, but useful for role-checks
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.user.username








class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now() + timedelta(days=30))
    renew_count = models.IntegerField(default=0)
    returned = models.BooleanField(default=False)

    def renew(self):
        if self.renew_count < 1:
            self.due_date += timedelta(days=30)
            self.renew_count += 1
            self.save()
