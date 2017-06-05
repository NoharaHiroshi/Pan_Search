# coding=utf-8

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from search.models import SearchResult
from django.views.decorators.csrf import csrf_exempt


def index(request):
    result = {
        'response': 'ok',
        'info': ''
    }
    try:
        count = SearchResult.objects.count()
        result['count'] = count if count else 0
        return render(request, 'search/index.html', result)
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
    except Exception as ue:
        raise Http404(u"网站出现错误，请联系管理员")


@csrf_exempt
def create_record(request):
    result = {
        'response': 'ok',
        'info': '',
    }
    try:
        if request.method == 'POST':
            req = json.loads(request.body)
            keyword = req.get('keyword', None)
            customer_id = req.get('customer_id', None)
            resource_id = req.get('resource_id', None)
            print resource_id
        else:
            result.update({
                'response': 'fail',
                'info': 'This is a POST method'
            })
        context = json.dumps(result, ensure_ascii=False)
        return HttpResponse(context, content_type="application/json")
    except Exception as ue:
        raise Http404(u"网站出现错误，请联系管理员")