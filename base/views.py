from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from base.models import Lounge, Message, Topic
from base.forms import AuthForm, LoungeForm, UserForm

def home(request):
	return render(request, 'base/home.html', {})

def profile(request, id):
	data = User.objects.get(id=id)
	lounges = data.lounge_set.all()
	msgs = data.message_set.all()
	param = {
		'data': data,
		'lounges': lounges,
		'msgs': msgs,
	}
	return render(request, 'base/profile.html', param)

@login_required(login_url='auth')
def profile_edit(request, id):
	data = User.objects.get(id=id)
	form = UserForm(instance=data)
	if request.user.id != data.id:
		messages.error(request, 'You are not allowed to do that...')
		return redirect('home')
	if request.method == 'POST':
		form = UserForm(request.POST, instance=data)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated successfully...')
			return redirect('profile', id=data.id)
		else:
			print(form.errors.as_data())
	param = {
		'form': form,
	}
	return render(request, 'base/profile-form.html', param)

def auth(request):
	page = 'login'
	if request.user.is_authenticated:
		messages.warning(request, 'You have been signed in already...')
		return redirect('home')
	form = AuthForm()
	if request.method == 'POST':
		uname = request.POST.get('username').lower()
		paswd = request.POST.get('password')
		try:
			chk = authenticate(request, username=uname, password=paswd)
			if chk is not None:
				login(request, chk)
				messages.success(request, 'Successfully signed in...')
				return redirect('home')
			else:
				messages.warning(request, 'USER or PASS does not match...')
		except:
			messages.error(request, 'USER: @'+uname+' does not exist...')
	param = {
		'form': form,
		'page': page,
	}
	return render(request, 'base/auth.html', param)

def register(request):
	page = 'register'
	form = UserCreationForm()

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			authenticate()
			login(request, user)
			messages.success(request, 'Welcome, @'+user.username+'!')
			return redirect('home')
		else:
			messages.error(request, 'There is an error occurred...')
	param = {
		'form': form,
		'page': page,
	}
	return render(request, 'base/auth.html', param)

def destroy(request):
	logout(request)
	messages.success(request, 'You have been signed out...')
	return redirect('home')

def lounge(request):
	members = User.objects.all().order_by('username')[0:3]
	member_count = members.count()
	query = request.GET.get('query', '')
	tag = request.GET.get('tag', '')
	page_num = request.GET.get('page', 1)
	topics = Topic.objects.all().order_by('name')
	recent_updates = Message.objects.filter(Q(lounge__topic__name__icontains=tag) or Q(lounge__topic__name__icontains=query))

	if query != '':
		lounges = Lounge.objects.filter(Q(topic__name__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query) | Q(host__username__icontains=query))
	elif query == '' and tag != '':
		lounges = Lounge.objects.filter(Q(topic__name__icontains=tag))
	elif query != '' and tag != '':
		messages.warning(request, 'Currently unavailable...')
		return HttpResponseRedirect('/lounge/')
	else:
		lounges = Lounge.objects.all()

	paginator = Paginator(lounges, 4)
	counter = Lounge.objects.all().count()
	try:
		pages = paginator.page(page_num)
	except PageNotAnInteger:
		pages = paginator.page(1)
	except EmptyPage:
		pages = paginator.page(paginator.num_pages)

	pages_range = pages.paginator.page_range
	param = {
		'all_lounges_count': counter,
		'lounges': lounges,
		'member_count': member_count,
		'members': members,
		'pages': pages,
		'pages_range': pages_range,
		'recent_updates': recent_updates,
		'tag': tag,
		'topics': topics,
		'query': query,
	}
	return render(request, 'base/lounge.html', param)

def lounge_details(request, id):
	each = Lounge.objects.get(id=id)
	msgs = each.message_set.all().order_by('-created')
	parties = each.participants.all()
	topics = Topic.objects.all()
	if request.method == 'POST':
		dialogue = Message.objects.create(
			user = request.user,
			lounge = each,
			body = request.POST.get('comets'),
		)
		each.participants.add(request.user)
		return redirect('lounge_details', id=each.id)
	param = {
		'lounge': each,
		'msgs': msgs,
		'parties': parties,
		'topics': topics,
	}
	return render(request, 'base/lounge-details.html', param)

@login_required(login_url='auth')
def lounge_insert(request):
	if request.method == 'POST':
		form = LoungeForm(request.POST)
		if form.is_valid():
			lounge = form.save(commit=False)
			lounge.host = request.user
			lounge.save()
			lounge.participants.add(request.user)
			messages.success(request, 'Successfully posted...')
			return HttpResponseRedirect('/lounge/')
	else:
		form = LoungeForm()
	param = {
		'form': form,
	}
	return render(request, 'base/lounge-form.html', param)

@login_required(login_url='auth')
def lounge_edit(request, id):
	lounge = Lounge.objects.get(id=id)
	form = LoungeForm(instance=lounge)
	if request.user != lounge.host:
		messages.error(request, 'You are not allowed to do that...')
		return HttpResponseRedirect('/lounge/')
	if request.method == 'POST':
		form = LoungeForm(request.POST, instance=lounge)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/lounge/')
	param = {
		'form': form,
	}
	return render(request, 'base/lounge-form.html', param)

@login_required(login_url='auth')
def lounge_delete(request, id):
	data = Lounge.objects.get(id=id)
	if request.user != data.host:
		messages.error(request, 'You are not allowed to do that...')
	else:
		data.delete()
		messages.success(request, 'Successfully deleted...')
	return HttpResponseRedirect('/lounge/')


@login_required(login_url='auth')
def msg_delete(request, id):
	msg = Message.objects.get(id=id)
	lounge_id = request.GET.get('lounge')
	if request.user != msg.user:
		messages.error(request, 'You are not supposed to do that...')
		return redirect('lounge_details', id=lounge_id)
	else:
		msg.delete()
		messages.success(request, 'Successfully deleted...')
		return redirect('lounge_details', id=lounge_id)
	return True

def rps(request):
	return render(request, 'base/rps.html')

def task(request):
	param = {
		'asd': 'asd',
	}
	return render(request, 'base/taskmaster.html', param)