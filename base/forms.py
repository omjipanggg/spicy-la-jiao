from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from base.models import Topic, Lounge, Message

class LoungeForm(ModelForm):
	"""docstring for LoungeForm"""
	class Meta:
		model = Lounge
		fields = '__all__'
		exclude = [
			'host',
			'participants',
		]

class UserForm(ModelForm):
	# """docstring for UserForm"""
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			'email',
		]

class AuthForm(ModelForm):
	"""docstring for AuthForm"""
	class Meta:
		model = User
		fields = [
			'username',
			'password',
		]
		help_texts = { 
			'username': None,
			'password': None,
		}
		widgets = {
			'username': forms.TextInput(
				attrs = {
					'autocomplete': 'off',
					'autofocus': 'true',
				},
			),
			'password': forms.PasswordInput(
				attrs = {
					'autocomplete': 'off',
				},
			),
		}