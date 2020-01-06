from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import CardForm

from .models import *
from accounts.models import Profile
from django.db.models import Q
# Create your views here.


def trade(request, id):
    user_profile = Profile.objects.get(user_id=request.user.id)
    card_traded = Cards.objects.get(id=id)
    #Creating the transactions
    new_transac = Transactions(
        sender=user_profile,
        card_sent=card_traded,
        status="pending"
        )
    new_transac.save()

    #Delete the card put on the market in DeckCard of the sender
    deck_user = DeckUser.objects.get(profile=user_profile)
    criterion1 = Q(cards_id=id)
    criterion2 = Q(deck_id=deck_user.id)
    deck_card = DeckCard.objects.filter(criterion1&criterion2)
    deck_card[0].delete()
    messages.info(request, f"Your card is Now on the market")
    return redirect('profile', request.user.id)


def sale(request, id):
    card_sent = Cards.objects.get(id=id)
    sender_profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        price = request.POST.get('price')
        new_transaction = Transactions(
            sender = request.user.profile,
            status="pending",
            card_sent=card_sent,
            price=int(price)
            )
        new_transaction.save()

        # Delete the card put on the market in DeckCard of the sender
        deck_user = DeckUser.objects.get(profile=sender_profile)
        criterion1 = Q(cards_id=id)
        criterion2 = Q(deck_id=deck_user.id)
        deck_card = DeckCard.objects.filter(criterion1 & criterion2)
        deck_card[0].delete()
        messages.info(request, f"Your card is Now on the market")
        return redirect('profile', request.user.id)
    return render(request, 'sale_form.html', {'card':card_sent})


def all_transaction(request):
    transac=Transactions.objects.all()
    return render(request, 'all_transactions.html', {'transactions':transac})


def detail_transac(request, id):
    transaction = Transactions.objects.get(id=id)
    deck_receiver = DeckUser.objects.get(profile_id=request.user.profile.id)
    cards_to_received = DeckCard.objects.filter(deck_id=deck_receiver.id)
    if request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        context = RequestContext(request)
        transaction.card_received_id = selected_card
        transaction.receiver = request.user.profile
        transaction.status = "executed"
        transaction.save()

        #Make changes in deck of the receiver and sender(modify their deck cards and points)
        deck_receiver = DeckUser.objects.get(profile=request.user.profile)
        criterion1 = Q(cards_id=selected_card)
        criterion2 = Q(deck_id=deck_receiver.id)
        deckcard_receiver = DeckCard.objects.get(criterion1 & criterion2)
        deckcard_receiver.cards_id = transaction.card_sent.id
        deckcard_receiver.save()

        receiver_profile = Profile.objects.get(id=request.user.profile.id)
        receiver_profile.points += transaction.card_sent.xp
        receiver_profile.save()

        deck_sender = DeckUser.objects.get(profile=transaction.sender)
        new_deck_card_for_sender = DeckCard(
            quantity=1,
            cards_id = selected_card,
            deck_id=deck_sender.id
            )
        new_deck_card_for_sender.save()
        messages.success(request, f"Transaction done")
        return redirect('all_transactions')

    return render(request, 'details_transaction.html', {'transaction':transaction,
                                                        'receiver_cards':cards_to_received})


def pay_card(request, id):
    transaction=Transactions.objects.get(id=id)

    #Add coins to the sender
    sender_profile = Profile.objects.get(id=transaction.sender.id)
    sender_profile.coins+=transaction.price
    sender_profile.save()
    #Retrieve coins to the receiver and add points to the receiver, add the card to the receiver
    receiver_profile = Profile.objects.get(id=request.user.profile.id)
    receiver_profile.coins-=transaction.price
    receiver_profile.points+=transaction.card_sent.xp
    receiver_profile.save()
    receiver_deck=DeckUser.objects.get(profile=receiver_profile)
    new_deckcard_receiver = DeckCard(
        quantity=1,
        cards=transaction.card_sent,
        deck=receiver_deck
        )
    new_deckcard_receiver.save()
    # Save the receiver of the transaction
    transaction.receiver = request.user.profile
    transaction.status = 'executed'
    transaction.save()
    messages.success(request, f"Congratulations you earned a New card and more points")
    return redirect('all_transactions')


def abort_transac(request, id):
    transaction = Transactions.objects.get(id=id)
    #Put the card back to the sender
    deck_sender = DeckUser.objects.get(profile=transaction.sender)
    reload_sender_card = DeckCard(
        quantity=1,
        cards = transaction.card_sent,
        deck = deck_sender
        )
    reload_sender_card.save()
    transaction.delete()
    messages.success(request, f"Your card is back and your transaction has been deleted")
    return redirect('all_transactions')


def leader(request):
    all_profiles = Profile.objects.all().order_by("-points", "-coins")[:4]
    # counter = Profile.objects.all().count()
    # dico = {counter:all_profiles}
    winner = Profile.objects.order_by("-points")[0]
    return render(request, 'leader.html', {'profiles':all_profiles,
                                           'winner':winner})


def delete_transac(request, id):
    old_transac = Transactions.objects.get(id=id)
    deck_sender = DeckUser.objects.get(profile=old_transac.sender)
    reload_sender_card = DeckCard(
        quantity=1,
        cards=old_transac.card_sent,
        deck=deck_sender
        )
    reload_sender_card.save()
    old_transac.delete()
    messages.info(request, f"Transaction has been deleted")
    return redirect('all_transactions')


def cards(request):
    cards = Cards.objects.all().order_by("-xp")
    total = Cards.objects.all().count()
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"New Card added")
            return redirect('cards')
    else:
        form = CardForm()
    return render(request,'all_cards.html', {'cards':cards,
                                             'total':total,
                                             'form':form})


def delete_card(request, id):
    card=Cards.objects.get(id=id)
    card.delete()
    messages.info(request, f"Card deleted")
    return redirect('cards')
