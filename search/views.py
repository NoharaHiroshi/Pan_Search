from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render


def index(request):
    context = {
        'response': 'ok',
        'info': ''
    }
    try:
        return render(request, 'index.html', context)
    except Exception as e:
        print e
