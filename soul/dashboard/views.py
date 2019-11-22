from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from urllib.parse import quote

# Create your views here.

'''
def home(request):
    return HttpResponse('<h1>SOUL</h1>')
'''


def home(request):
    return render(request, 'dashboard/dashboard.html', {'name': 'Goutham'})


def add(request):
    val1 = request.POST['num1']
    val2 = request.POST['num2']
    res = int(val1) + int(val2)
    return render(request, 'dashboard/result.html', {'result': res})


def getData(request):
    temp = request.GET['q']
    q = quote(temp)
    url = 'http://18.223.109.186:8983/solr/IRF19P1/select?q=text_en%3A' + q
    data = urlopen(url)

    tweets = json.load(data)['response']['docs']
    name = ""
    if len(tweets) >0:
        name = tweets[0]['user.screen_name'][0]



    return render(request, 'dashboard/result.html', {'tweets': tweets , 'name': name})


