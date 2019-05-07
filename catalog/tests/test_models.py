from django.test import TestCase

from catalog.models import Author, Book, Genre, Language

class AuthorModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    # data for all test methods in this class
    Author.objects.create(first_name='Nathan', last_name='Magyar')
  
  def test_first_name_label(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('first_name').verbose_name
    self.assertEquals(field_label, 'first name')
  
  def test_date_of_birth(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('date_of_birth').verbose_name
    self.assertEquals(field_label, 'date of birth')
  
  def test_date_of_death(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('date_of_death').verbose_name
    self.assertEquals(field_label, 'date of death')
  
  def test_first_name_max_length(self):
    author = Author.objects.get(id=1)
    max_length = author._meta.get_field('first_name').max_length
    self.assertEquals(max_length, 100)
  
  def test_last_name_max_length(self):
    author = Author.objects.get(id=1)
    max_length = author._meta.get_field('last_name').max_length
    self.assertEquals(max_length, 100)
  
  def test_object_name_is_first_and_last(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEquals(expected_object_name, str(author))

  def test_get_absolute_url(self):
      author = Author.objects.get(id=1)
      # This will also fail if the urlconf is not defined.
      self.assertEquals(author.get_absolute_url(), '/catalog/authors/1/')

class BookModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    author = Author.objects.create(first_name='Nathan', last_name='Magyar')
    genre = Genre.objects.create(name='Awesomeness')
    language = Language.objects.create(name='Awesomese')
    Book.objects.create(
      title='My Awesome Book', 
      author=author,
      summary='Its basically the best thing every written. Like. Ever.',
      isbn='1234567891011',
      language=language,
    )
    Book.objects.get(id=1).genre.set([genre])

  def test_title_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('title').verbose_name
    self.assertEquals(field_label, 'title')
  
  def test_title_max_length(self):
    book = Book.objects.get(id=1)
    max_length = book._meta.get_field('title').max_length
    self.assertEquals(max_length, 200)
  
  def test_book_object_name_is_title(self):
    book = Book.objects.get(id=1)
    expected_name = f'{book.title}'
    self.assertEquals(expected_name, str(book))
  
  def test_summary_max_length(self):
    book = Book.objects.get(id=1)
    max_length = book._meta.get_field('summary').max_length
    self.assertEquals(max_length, 1000)

  def test_isbn_max_length(self):
    book = Book.objects.get(id=1)
    max_length = book._meta.get_field('isbn').max_length
    self.assertEquals(max_length, 13)