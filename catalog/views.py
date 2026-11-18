from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=BookInstance.LoanStatus.AVAILABLE).count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list' # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='book')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html' # Specify your own template name/location


class MyView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class BookDetailView(generic.DetailView):
    model = Book

def bool_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

def bool_detail_view2(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', {'book': book})

