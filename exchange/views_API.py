from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import requests
import urllib.parse


class ResponseAPI(APIView):
    def get(self, request):
        from_currency = request.GET.get('from')
        to_currency = request.GET.get('to')
        val = int(request.GET.get('value'))

        url = "https://currate.ru/api/?"
        pair = from_currency + to_currency
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

        converted_amount = val * float(rate)
        context = {
            'result': converted_amount,
        }
        return Response(context, status=status.HTTP_200_OK)
