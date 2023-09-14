from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.views.decorators.cache import cache_page
import requests

# функция дает ответ по api


@api_view(('GET',))
def exchange_api(request):
    if request.method == "GET":
        from_currency = request.GET.get('from')
        to_currency = request.GET.get('to')
        val = int(request.GET.get('value'))
        pair = from_currency + to_currency

        req = "https://currate.ru/api/?get=rates&pairs=" + \
            pair + "&key=3259fd1fd93cf66b126c1626ae9c850a"

        response = requests.get(url=req).json()
        get_rate = response.get("data")
        try:
            rate = get_rate[pair]
        except TypeError:
            rate = 0

        converted_amount = val * float(rate)
        context = {
            'result': converted_amount,
        }
        return Response(context, status=status.HTTP_200_OK)


# получаем список возможных валют
@cache_page(60 * 15)
def get_currencies(request):
    response = requests.get(
        url="https://currate.ru/api/?get=currency_list&key=3259fd1fd93cf66b126c1626ae9c850a").json()
    currencies = response.get("data")

    tmp = set()
    # в ответе приходят пары валют на подобие RUBEUR, поэтому вначале почистим
    # и выделим уникальные
    for cur in currencies:
        new = cur[:3]
        tmp.add(new)
    return list(tmp)


# класс для графической формы
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
        req = "https://currate.ru/api/?get=rates&pairs=" + \
            pair + "&key=3259fd1fd93cf66b126c1626ae9c850a"
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
