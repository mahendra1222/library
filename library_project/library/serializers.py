from rest_framework import serializers
from .models import Book, Student, Loan, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']


class BookSerializer(serializers.ModelSerializer):
    available_copies = serializers.SerializerMethodField()
    next_available_date = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'copies', 'available_copies', 'next_available_date']

    def get_available_copies(self, obj):
        loans = Loan.objects.filter(book=obj, returned=False)
        return obj.copies - loans.count()

    def get_next_available_date(self, obj):
        loan = Loan.objects.filter(book=obj, returned=False).order_by('due_date').first()
        return loan.due_date if loan else None


class ExtendedLoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    student_name = serializers.ReadOnlyField(source='student.name')

    class Meta:
        model = Loan
        fields = ['book', 'book_title', 'student', 'student_name', 'issue_date', 'due_date', 'renew_count']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
#

#
# class LoanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Loan
#         fields = '__all__'
#
# def validate(self, data):
#     """
#     Check that the student hasn't exceeded the book limit.
#     """
#     student = data['student']
#     if Loan.objects.filter(student=student).count() >= 10:
#         raise serializers.ValidationError("This student has already borrowed 10 books.")
#     return data
