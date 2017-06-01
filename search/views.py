# coding=utf-8

import json
from django.shortcuts import render
from django.http import HttpResponse
from search.models import SearchResult
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import RequestContext, render_to_response


def index(request):
    context = {
        'response': 'ok',
        'info': ''
    }
    try:
        return render(request, 'index.html', context)
    except Exception as e:
        print e


@csrf_protect
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
            return render_to_response(context=context, context_instance=RequestContext(request), content_type="application/json")
        else:
            return 'this is a POST method'
    except Exception as e:
        print e
