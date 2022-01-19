from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.forms import ModelForm
from .models import Ticket, Review

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class TicketForm(ModelForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.form_method = 'POST'
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Nom du livre',
            'description': 'Description',
            'image': 'Ajouter une image'
        }  
class ReviewForm(ModelForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.form_method = 'POST'
    class Meta:
        model = Review
        fields = '__all__'