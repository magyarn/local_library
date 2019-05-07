from django.urls import path
from . import views

app_name='catalog'

urlpatterns = [
  path('', views.index, name='index'),
  path('books/', views.BookListView.as_view(), name="book-list"),
  path('books/<int:pk>/', views.BookDetailView.as_view(), name="book-detail"),
  path('authors/', views.AuthorListView.as_view(), name="author-list"),
  path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name="author-detail"),
  path('my-books/', views.LoanedBooksByUserListView.as_view(), name='my-books'),
  path('borrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
  path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [  
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]

urlpatterns += [  
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]

urlpatterns += [  
    path('book-instance/<int:pk>/create/', views.BookInstanceCreateView.as_view(), name='book-instance-create'),
    path('book-instance/<uuid:pk>/update/', views.BookInstanceUpdateView.as_view(), name='book-instance-update'),
    path('book-instance/<uuid:pk>/delete/', views.BookInstanceDeleteView.as_view(), name='book-instance-delete'),
]