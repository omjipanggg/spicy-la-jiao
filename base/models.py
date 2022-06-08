from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Lounge(models.Model):
	host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	participants = models.ManyToManyField(User, related_name='participants', blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		ordering = [
			'-updated',
			'-created',
		]

	def __str__(self):
		return self.name

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	lounge = models.ForeignKey(Lounge, on_delete=models.CASCADE)
	body = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		ordering = [
			'-updated',
			'-created',
		]

	def __str__(self):
		return self.body