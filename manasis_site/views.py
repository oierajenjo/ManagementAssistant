from django.shortcuts import render

import csv
import json

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from .forms import *
from .models import Profile


def index(request):
    if not request.user.is_authenticated:
        return render(request, "landing.html")

    return profileView(request)


@login_required(login_url='login')
def profileView(request, pk=None):
    custom = Tag.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)

    context = {
        "tags": custom,
        "profile": profile,
        "share_text": f"Check {profile.user.username}'s profile on #GameHoarder"
    }

    return render(request, "account/profileView.html", context)


@login_required(login_url='login')
def download_csv(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        data = request.POST.getlist("data")

        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % request.POST.get("filename")

        writer = csv.writer(response)

        headers = json.loads(data[0].replace("'", '"'))
        writer.writerow(headers.keys())

        for row in data:
            title = json.loads(row.replace("'", '"'))

            if 'original_title' in title:
                title["game"] = title["original_title"]
                title.pop("original_title")

            writer.writerow(list(title.values()))

        return response


def login_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.last()
            default = Group.objects.get(name="standard_user")
            user.groups.add(default)
            user.save()
            return HttpResponseRedirect('login')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # faster than len()
                    if Profile.objects.filter(user=user).count() == 0:
                        profile = Profile(user=user)
                        profile.save()
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = UserForm

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'registration/login_register.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("login")


@login_required(login_url='login')
def ajax_users(request):
    username = request.GET['username']

    initial = Profile.objects.filter(Q(user__first_name__contains=username) | Q(user__username__contains=username)
                                     | Q(user__last_name__contains=username)).exclude(user=request.user)

    initial = list(initial.values())

    following = request.GET['following']

    profiles = []
    for i in initial:
        if following == "no":
            if i.pk not in Profile.objects.get(user=request.user).friends.reverse().get().pk:
                profiles.append(i)
        else:
            profiles.append(i)

    codes = [i['user_id'] for i in profiles]
    print(codes)
    context = {"new_profiles": codes}
    return JsonResponse(context)


@login_required(login_url='login')
def search_user(request):
    custom = Tag.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.all().exclude(user=request.user)

    context = {
        "tags": custom,
        "profile": profile,
        "profiles": profiles
    }

    return render(request, "search/search_friends.html", context)


@login_required(login_url='login')
def search(request):
    custom = Tag.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    # multiple-choice values
    choices = ['genres', 'platforms']
    # all values except those
    params = {k: v for k, v in request.GET.dict().items() if k[:-2] not in choices}

    # check if external API should be used
    use_api = False
    try:
        use_api = params.pop('use_api')
        use_api = use_api == "true"
    except KeyError:
        pass

    # extract multiple-choice values
    for choice in choices:
        if f'{choice}[]' in request.GET.keys():
            params[choice] = request.GET.getlist(f'{choice}[]')

    # if query is empty, don't search
    if not GameHoarderDB.params_empty(params):
        games = GameHoarderDB.search(params, use_api=use_api)
    else:
        games = None

    games_wrapper = []
    games = list(games) if games else []
    for i in range(len(games)):
        games_wrapper.append(
            {
                'game': games[i],
                'developers': ' | '.join(dev.name for dev in games[i].parent_game.developers.all()),
                'publishers': ' | '.join(pub.name for pub in games[i].parent_game.publishers.all())
            }
        )

    platforms = [p.get('name') for p in Platform.objects.order_by().values('name').distinct()]
    genres = [g.get('name') for g in Genre.objects.order_by().values('name').distinct()]

    return render(request, 'search/search_form.html', {
        'first_platform': platforms[0] if len(platforms) > 0 else None,
        'first_genre': genres[0] if len(genres) > 0 else None,
        'platforms': platforms[1:] if len(platforms) > 1 else [],
        'genres': genres[1:] if len(genres) > 1 else [],
        'games': games_wrapper,
        'user': request.user.interested_set,
        "tags": custom,
        "profile": profile,
    })


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
