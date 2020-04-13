from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "landing.html")

    return profileView(request)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("login")


@login_required(login_url='login')
def edit_user(request):
    custom = Tag.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = User_Avatar_Form(request.POST, request.FILES, instance={
            'user': request.user,
            'avatar': Profile.objects.get(user=request.user),
        })
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = User_Avatar_Form
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'account/edit_user.html',
                  {'tags': custom, 'user': request.user, 'profile': profile})
