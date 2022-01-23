from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

from django.forms import ModelForm
from .models import *
from crispy_forms.bootstrap import InlineRadios

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_method = 'POST'
        
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
        
        labels = {
            'headline': 'Titre de la critique',
            'rating': 'Note sur 5',
            'body': 'Critique'
        }  
        
class UserFollowsForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = '__all__'
        
