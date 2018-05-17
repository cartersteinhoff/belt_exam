from django.shortcuts import render, redirect
from django.contrib import messages
from ..LoginReg.models import User
from .models import Friend
from django.db.models import Q


# Create your views here.

def index(request):
    print('Index Route')
    return render(request, 'index.html')


# login user
def login(request):
    # get user data from post request form
    result = User.objects.validate_login(request.POST)

    # check for errors in login validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect(index)

    # if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect(friends)


# logout user
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect(index)


# register user
def register(request):
    # get user data from post request form
    result = User.objects.validate_registration(request.POST)

    # check for errors in registration validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        try:
            del request.session['user_id']
        except KeyError:
            pass

        return redirect(index)

    # if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect(friends)


def friends(request):
    print(User.objects.filter(user__user_id=request.session['user_id']))
    user = User.objects.get(id=request.session['user_id'])
    user_all = User.objects.exclude(Q(user__user_id=request.session['user_id']) | Q(user__friend_id=request.session['user_id'])).exclude(id=request.session['user_id'])
    friends_all = Friend.objects.filter(user_id=request.session['user_id'])
    # friend_filter = Friend.objects.all().filter(Q(poker=user_id) | Q(poked=user_id)).order_by('pokedate'),
    context = {
        'user': user,
        'user_all': user_all,
        'friends_all': friends_all
    }
    return render(request, 'friends.html', context)


def add_friend(request, id):
    print('Add Friend Route')
    user_id = User.objects.get(id=request.session['user_id'])
    friend_id = User.objects.get(id=id)
    request.session['friend_id'] = id
    Friend.objects.create_friend(user_id, friend_id)
    return redirect(friends)

def remove_friend(request, id):
    print('Remove Friend Route')
    print(id)
    user_id = User.objects.get(id=request.session['user_id'])
    friend_id = User.objects.get(id=id)

    Friend.objects.delete_friend(user_id, friend_id)

    return redirect(friends)


def user_profile(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'user.html', context)
