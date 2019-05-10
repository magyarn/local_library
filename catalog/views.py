import datetime

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.models import Book, Author, BookInstance, Genre, Language
from catalog.forms import RenewBookModelForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    num_and = Book.objects.all().filter(title__icontains='and').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Queryset of newest books in the system
    newest_books = Book.objects.all().order_by('-created_at')[:4]
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_and': num_and,
        'num_visits': num_visits,
        'newest_books': newest_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  paginate_by = 3

class BookDetailView(generic.DetailView):
  model = Book

class AuthorListView(generic.ListView):
  model = Author
  paginate_by = 3

class AuthorDetailView(generic.DetailView):
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  """Lists books loaned to current user."""
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 3

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
  permission_required = 'catalog.can_mark_returned'
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_all.html'
  paginate_by = 3

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreateView(PermissionRequiredMixin, CreateView):
  permission_required = 'catalog.add_author'
  model = Author
  fields = '__all__'

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
  permission_required = 'catalog.change_author'
  model = Author
  fields = '__all__'

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
  permission_required = 'catalog.delete_author'
  model = Author
  success_url = reverse_lazy('catalog:author-list')

class BookCreateView(PermissionRequiredMixin, CreateView):
  permission_required = 'catalog.add_book'
  model = Book
  fields = '__all__'

class BookUpdateView(PermissionRequiredMixin, UpdateView):
  permission_required = 'catalog.change_book'
  model = Book
  fields = '__all__'

class BookDeleteView(PermissionRequiredMixin, DeleteView):
  permission_required = 'catalog.delete_book'
  model = Book
  success_url = reverse_lazy('catalog:book-list')

class BookInstanceCreateView(PermissionRequiredMixin, CreateView):
  permission_required = 'catalog.add_bookinstance'
  model = BookInstance
  fields = ['id', 'imprint', 'status']
  success_url = reverse_lazy('catalog:book-detail')

  def get_initial(self):
    """Return the initial data to use for forms on this view."""
    # Get the initial dictionary from the superclass method
    initial = super(BookInstanceCreateView, self).get_initial()
    # Copy the dictionary so we don't accidentally change a mutable dict
    initial = initial.copy()
    book = Book.objects.filter(pk=self.kwargs['pk'])[0].pk
    initial['book'] = book
    return initial
  
  def get_context_data(self, **kwargs):
    book = Book.objects.filter(pk=self.kwargs['pk'])[0]
    context = super(BookInstanceCreateView, self).get_context_data()
    context['book_title'] = book.title
    context['book_author'] = book.author
    return context
  
  def form_valid(self, form):
    super(BookInstanceCreateView, self).form_valid(form)
    obj = form.save(commit=False)
    obj.book = Book.objects.filter(pk=self.kwargs['pk'])[0]
    obj.save()
    return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self):
    return reverse('catalog:book-detail', kwargs={ 'pk': self.kwargs['pk'] })

class BookInstanceUpdateView(PermissionRequiredMixin, UpdateView):
  permission_required = 'catalog.change_bookinstance'
  model = BookInstance
  fields = ['id', 'imprint', 'status', 'due_back']

  def get_success_url(self):
    bookinstance = BookInstance.objects.filter(id=self.kwargs['pk'])[0]
    return reverse('catalog:book-detail', kwargs={ 'pk': bookinstance.book.pk })

class BookInstanceDeleteView(PermissionRequiredMixin, DeleteView):
  permission_required = 'catalog.delete_bookinstance'
  model = BookInstance

  def get_success_url(self):
    bookinstance = BookInstance.objects.filter(id=self.kwargs['pk'])[0]
    return reverse('catalog:book-detail', kwargs={ 'pk': bookinstance.book.pk })
    
