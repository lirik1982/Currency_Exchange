from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.decorators import api_view


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
        except:
            rate = 0

        converted_amount = val * float(rate)
        context = {
            'result': converted_amount,
        }
        return Response(context, status=status.HTTP_200_OK)


def exchange(request):
    response = requests.get(
        url="https://currate.ru/api/?get=currency_list&key=3259fd1fd93cf66b126c1626ae9c850a").json()
    currencies = response.get("data")
    tmp = []
    for cur in currencies:
        new = cur[:3]
        if new in tmp:
            continue
        else:
            tmp.append(new)

    if request.method == "POST":
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
        except:
            rate = 0
        converted_amount = from_amount * float(rate)
        context = {
            'currencies': tmp,
            'converted_amount': converted_amount,
            'from_amount': from_amount,
        }
    else:
        context = {
            'currencies': tmp,
        }

    return render(
        request=request,
        template_name="index.html",
        context=context
    )
