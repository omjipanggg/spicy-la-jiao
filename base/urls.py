from django.urls import path
from base.views import *

urlpatterns = [
	path('', home, name='home'),
	
	path('auth/', auth, name='auth'),
	path('register/', register, name='register'),
	path('destroy/', destroy, name='destroy'),

	path('lounge/', lounge, name='lounge'),
	path('lounge/<id>/', lounge_details, name='lounge_details'),
	path('lounge_insert/', lounge_insert, name='lounge_insert'),
	path('lounge/<id>/edit/', lounge_edit, name='lounge_edit'),
	path('lounge/<id>/delete/', lounge_delete, name='lounge_delete'),

	path('message/<id>/delete/', msg_delete, name='msg_delete'),

	path('profile/<id>/', profile, name='profile'),
	path('profile/<id>/edit/', profile_edit, name='profile_edit'),

	path('rps/', rps, name='rps'),

	path('task/', task, name='task'),
]