from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render
from django.http import HttpResponse
from search.models import SearchResult


def index(request):
    context = {
        'response': 'ok',
        'info': ''
    }
    try:
        return render(request, 'index.html', context)
    except Exception as e:
        print e


def search(request):
    result = {
        'response': 'ok',
        'info': '',
        'search_result_list': list()
    }
    try:
        if request.method == 'POST':
            search_info = request.POST.get('search', None)
            all_query = SearchResult.objects.filter(
                name=search_info
            )
            if all_query:
                search_result_list = list
                for query in all_query:
                    search_dict = query.to_ict()
                    search_result_list.append(search_dict)
                result['search_result_list'] = search_result_list
            else:
                result['info'] = 'no result get'
            context = json.dumps(result)
            return HttpResponse(context, content_type="application/json")
        else:
            return 'this is a POST method'
    except Exception as e:
        print e