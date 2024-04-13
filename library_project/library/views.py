from datetime import timezone, timedelta
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Student, Loan, UserProfile
from .serializers import BookSerializer, ExtendedLoanSerializer, StudentSerializer, UserProfileSerializer
from rest_framework import permissions
from .permissions import IsLibrarian, IsStudent


# class BookViewSet(viewsets.ReadOnlyModelViewSet):
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentLoansViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExtendedLoanSerializer

    # permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(student__user=user)


@api_view(['POST'])


def borrow_book(request, book_id):
    student = get_object_or_404(Student, user=request.user)
    book = get_object_or_404(Book, pk=book_id)

    if student.borrowingrecord_set.count() >= 10:
        return Response({'message': 'You have reached the maximum limit of borrowed books.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if book.num_copies > 0:
        borrowing_record = Loan.objects.create(
            student=student,
            book=book,
            borrowing_date=timezone.now(),
            return_date=timezone.now() + timedelta(days=30)
        )
        book.num_copies -= 1
        book.save()
        serializer = ExtendedLoanSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Sorry, this book is currently unavailable for borrowing.'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def borrowed_books(request):
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        borrowing_records = Loan.objects.filter(student=student)
        serializer = ExtendedLoanSerializer(borrowing_records, many=True)  # Use serializer if needed
        return Response(serializer.data)


class ManageLoansViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = ExtendedLoanSerializer

    # permission_classes = [permissions.IsAuthenticated, IsLibrarian]

    def perform_create(self, serializer):
        serializer.save(librarian=self.request.user)



class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
