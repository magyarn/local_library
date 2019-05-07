import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.validators import ValidationError

from catalog.forms import RenewBookModelForm

class RenewBookFormTest(TestCase):
  def test_renew_form_date_field_label(self):
    form = RenewBookModelForm()
    # We also have to test whether the label value is None, 
    # because even though Django will render the correct label 
    # it returns None if the value is not explicitly set.
    self.assertTrue(form.fields['due_back'].label == None or form.fields['due_back'].label == 'Renewal date')
  
  def test_renew_form_date_field_help_text(self):
    form = RenewBookModelForm()
    self.assertEqual(form.fields['due_back'].help_text, 'Enter a date between now and 4 weeks (default 3).')
  
  def test_renew_form_date_in_past(self):
    date = datetime.date.today() - datetime.timedelta(days=1)
    form = RenewBookModelForm(data={'due_back': date})
    self.assertFalse(form.is_valid())
  
  def test_renew_form_date_too_far_in_future(self):
    date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
    form = RenewBookModelForm(data={'due_back': date})
    self.assertFalse(form.is_valid())
  
  def test_renew_form_date_today(self):
    date = datetime.date.today()
    form = RenewBookModelForm(data={'due_back': date})
    self.assertTrue(form.is_valid())
  
  def test_renew_form_date_max(self):
    date = timezone.now() + datetime.timedelta(weeks=4)
    form = RenewBookModelForm(data={'due_back': date})
    self.assertTrue(form.is_valid())