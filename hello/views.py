import requests
import json
import time

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from fidor import FidorClient


access_token = 'bb0c4de1ec6fda142d48991995f0dbaa'
api_url = 'https://aps.fidor.de'

def index(request):
    fidor = FidorClient(access_token, api_url)
    account = fidor.accounts.get(8)
    transactions = fidor.transactions.all(params={'per_page': 200 })
    
    savings = 0
    goal_cost = 1000
    magic_word = 'kaffe'

    for t in transactions['data']:
        if t['subject'] is not None:
            if t['subject'].find(magic_word) > -1 and t['amount'] > 0:
                savings = savings + t['amount']

    progress = (savings *100)/ goal_cost

    return render(request, 'index.html', {'account': account, 'transactions': transactions, 'progress': progress})

def transfer(request):
    fidor = FidorClient(access_token, api_url)

    #payload = {
    #    'account_id': 8,
    #    'amount': 1,
    #    'external_uid': int(time.time()),
    #    'receiver': '99996807',
    #    'currency': 'EUR',
    #    'subject': 'Tak for kaffe!'
    #}

    payload = {
        'account_id': 8,
        'amount': 100,
        'remote_iban': 'DE04333706726265131076',
        'external_uid': int(time.time()),
        'subject': 'Tak for kaffe!'
    }



    print fidor.sepa_credit_transfers.create(payload)
    account = fidor.accounts.get(8)
    transactions = fidor.transactions.all()

    return render(request,'transfer.html', 
        {'account': account, 'transactions': transactions})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

