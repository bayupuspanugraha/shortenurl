import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
from nanoid import generate
from .models import ShortenURL

port = 4545
baseURL = f'http://localhost:{port}'


def index():
    info = {
        'url_list': [
            {
                'url': '/info',
                'method': 'GET',
                'params': '',
                'body': '',
                'desc': 'Shows all data from database'
            },
            {
                'url': '/shortenurl',
                'method': 'POST',
                'params': '',
                'body': '{url: "YOUR_STRING_URL"}',
                'desc': 'Generates new short url from original url'
            },
            {
                'url': '/go/:id',
                'method': 'GET',
                'params': ':id => the shorten url id',
                'body': '',
                'desc': 'Access your ORIGINAL Url and redirect to the page'
            }
        ]
    }

    response = JsonResponse(
        {'message': '', 'data': info}, status=HTTPStatus.OK)

    return response


def go(request, id):
    if id == '':
        return JsonResponse({'message': 'BAD-REQUEST', 'data': ''}, status=HTTPStatus.BAD_REQUEST)

    found_data = ShortenURL.objects.get(id=id)
    if not found_data:
        return JsonResponse({'message': 'NOT-FOUND', 'data': ''}, status=HTTPStatus.NOT_FOUND)

    return HttpResponseRedirect(found_data.originalURL)


def info(request):
    allData = ShortenURL.objects.all()
    response = []
    for data in allData:
        response.append({
            'originalURL': data.originalURL,
            'shortURL': f'{baseURL}/go/{data.id}'
        })
    return JsonResponse({'message': '', 'data': response}, status=HTTPStatus.OK)


@csrf_exempt
def shortenurl(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        if body_unicode == '':
            return JsonResponse({'message': 'NOT-FOUND', 'data': ''},
                                status=HTTPStatus.NOT_FOUND)

        body = json.loads(body_unicode)
        url = body['url'] if 'url' in body else ''
        if url == '' or url == None:
            return JsonResponse({'message': 'NOT-FOUND', 'data': ''},
                                status=HTTPStatus.NOT_FOUND)

        newID = generate(size=10)

        newURL = ShortenURL(id=newID, originalURL=url)
        newURL.save()

        return JsonResponse({'message': '', 'data': {
            'originalURL': url,
            'shortURL': f'{baseURL}/go/{newID}'
        }}, status=HTTPStatus.OK)
    return JsonResponse({'message': 'NOT-FOUND', 'data': ''}, status=HTTPStatus.NOT_FOUND)
