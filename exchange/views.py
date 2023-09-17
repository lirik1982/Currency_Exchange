from django.shortcuts import render
from rest_framework.views import APIView

from django.core.cache import cache
import requests
import urllib.parse


# получаем список возможных валют
def get_currencies(request):
    cache_cur = cache.get('curr')
    if not cache_cur:
        response = requests.get(
            url="https://currate.ru/api/?get=currency_list&key=3259fd1fd93cf66b126c1626ae9c850a").json()
        currencies = response.get("data")
        tmp = set()
        # в ответе приходят пары валют на подобие RUBEUR,
        # поэтому вначале почистим и выделим уникальные
        for cur in currencies:
            new = cur[:3]
            tmp.add(new)
        cache.set('curr', list(tmp), 60)
        return list(tmp)
    else:
        return cache_cur


class Main(APIView):

    def get(self, request):
        tmp = get_currencies(request)
        context = {
            'currencies': tmp,
        }
        return render(
            request=request,
            template_name="index.html",
            context=context
        )

    def post(self, request):
        tmp = get_currencies(request)

        from_amount = float(request.POST.get('from_amount'))
        from_curr = request.POST.get('from_curr')
        to_curr = request.POST.get('to_curr')

        pair = from_curr + to_curr
        url = "https://currate.ru/api/?"
        params = {
            "get": "rates",
            "pairs": pair,
            "key": "3259fd1fd93cf66b126c1626ae9c850a",
        }
        req = url + urllib.parse.urlencode(params)

        response = requests.get(url=req).json()
        get_rate = response.get("data")
        try:
            rate = get_rate[pair]
        except TypeError:
            rate = 0
        converted_amount = from_amount * float(rate)
        context = {
            'currencies': tmp,
            'converted_amount': converted_amount,
            'from_amount': from_amount,
        }

        return render(
            request=request,
            template_name="index.html",
            context=context
        )
