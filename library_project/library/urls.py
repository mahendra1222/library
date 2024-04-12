from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('student', views.StudentViewSet, basename='student')
router.register('student_loans', views.StudentLoansViewSet, basename='student-loans')
router.register('manage_loans', views.ManageLoansViewSet, basename='manage-loans')
router.register('books', views.BookViewSet, basename='books')
# router.register('Available', views.borrowed_books, basename='available-books')
# router.register('take_book', views.borrow_book, basename='take-book')

# router.register(r'books', views.BookViewSet)
# router.register(r'students', views.StudentViewSet)
# router.register(r'loans', views.LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('available', views.borrowed_books,name='available-books'),
    path('take_book', views.borrow_book,    name='take-book'),
]
