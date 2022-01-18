from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import Ticket, Review

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'