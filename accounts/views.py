from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import Profile
from trading.models import Cards, DeckUser, DeckCard
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("before")
        if form.is_valid():
            print("valid")
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, Please configure your profile here!')
            return redirect('new_profile', username)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request, id):
    profile_user = Profile.objects.get(user_id=id)
    deck= DeckUser.objects.get(profile=profile_user)
    deck_card = DeckCard.objects.filter(deck=deck)
    counter = deck_card.count()
    dic = {50:'Barbarian King',40:'Archer Queen',30:'Battle Machine',20:'PEKKA',10:'Healer'}
    return render(request, 'profile.html', {'deckcards':deck_card,
                                             'dic':dic,
                                             'total':counter,
                                            'profile':profile_user})


def new_profile(request, username):
    #cards_id = Cards.objects.values_list('id')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            #We create the user profile
            new_profil = Profile(
                user=User.objects.get(username=username),
                personnage=form.cleaned_data['personnage'],
                profile_pic=form.cleaned_data['profile_pic'],
                points=form.cleaned_data['personnage']
                )
            new_profil.save()

            #We create the deck of the user
            new_deck = DeckUser(profile=new_profil)
            new_deck.save()

            #We compose the deck cards of the user
            cards_list = []
            for i in range(1, 7):
                cards_list.append(random.choice(Cards.objects.all()))

            for card in cards_list:
                new_deck_card = DeckCard(
                    cards=card,
                    deck=new_deck,
                    quantity=cards_list.count(card)
                    )
                new_deck_card.save()

            messages.success(request, f'Profile created succesfully!, You can now login')
            return redirect('login')
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})


def all_user(request):
    users = User.objects.all()
    return render(request, 'all_users.html', {'users':users})


def delete_user(request, id):
    old_user=User.objects.get(id=id)
    old_user.delete()
    messages.success(request, f"User deleted successfully")
    return redirect('all_user')
