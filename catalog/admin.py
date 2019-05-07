from django.contrib import admin

from catalog.models import Author, Genre, Language, Book, BookInstance

# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)

class BookInline(admin.StackedInline):
  model = Book
  extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
  model = BookInstance
  extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'display_genre')
  inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book', 'status', 'borrower', 'due_back')
  list_filter = ('status', 'due_back')