# coding=utf-8

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from search.models import SearchResult, KeyWordRecord
from django.views.decorators.csrf import csrf_exempt
from lib.id_generate import id_generate


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
    except Exception as e:
        raise Http404(u"网站出现错误，请联系管理员 %s" % e)


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
            resource_name = req.get('resource_name', None)
            if None not in [keyword, customer_id, resource_id, resource_name]:
                record = KeyWordRecord()
                record.id = id_generate()
                record.customer_id = customer_id
                record.keyword = keyword
                record.resource_id = resource_id
                record.resource_name = resource_name
                record.save()
            else:
                result.update({
                    'response': 'fail',
                    'info': 'Incomplete information'
                })
        else:
            result.update({
                'response': 'fail',
                'info': 'This is a POST method'
            })
        context = json.dumps(result, ensure_ascii=False)
        return HttpResponse(context, content_type="application/json")
    except Exception as e:
        raise Http404(u"网站出现错误，请联系管理员 %s" % e)