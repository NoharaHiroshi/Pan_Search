# coding=utf-8

import json
from django.shortcuts import render
from django.http import HttpResponse
from search.models import SearchResult
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {
        'response': 'ok',
        'info': ''
    }
    try:
        return render(request, 'index.html', context)
    except Exception as e:
        print e


@csrf_exempt
def search(request):
    result = {
        'response': 'ok',
        'info': '',
        'search_result_list': list()
    }
    try:
        if request.method == 'POST':
            search_info = json.loads(request.body).get('search', None)
            all_query = SearchResult.objects.filter(
                name__icontains=search_info
            )
            if all_query:
                search_result_list = list()
                for query in all_query:
                    search_dict = query.to_dict()
                    search_result_list.append(search_dict)
                result['search_result_list'] = search_result_list
            else:
                result['info'] = 'Unable to get search result'
        else:
            result.update({
                'response': 'fail',
                'info': 'This is a POST method'
            })
        context = json.dumps(result, ensure_ascii=False)
        return HttpResponse(context, content_type="application/json")
    except Exception as e:
        print e
