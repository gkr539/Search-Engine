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
    return render(request, 'dashboard/dashboard.html', {'name': 'Goutham','search_term':"search",'language':["English","Hindi","Portugese"],'Country':["India","USA","Brazil"]})

def getData(request):

    temp = request.GET['q']
    language = request.GET.get('language')
    country = request.GET.get('country')
    q = quote(temp)
    language=quote(language)
    if language == 'English':
        lang='en'
    elif language == 'Hindi':
        lang='hi'
    elif language == 'Portugese':
        lang = 'pt'
    else:
        lang="Choose.."
    
    if lang in ['en','hi','pt']:
        lang_filter='%20AND%20'+'lang%3A('+lang+')'
    else:
        lang_filter=""

    if country in ['India','USA','Brazil']:
        country_filter='%20AND%20'+'country%3A('+country+')'
    else:
        country_filter="Choose..."
    #place=quote(place)
    url = 'http://18.223.109.186:8983/solr/IRF19P1/select?q=(text_en%3A('+q+')%20OR%20'+'text_hi%3A('+q+')%20OR%20'+'text_pt%3A('+q+')%20OR%20'+'full_text%3A('+q+'))'+lang_filter+country_filter+'&wt=json&indent=true&rows=300'
    print(url)
    data = urlopen(url)

    tweets = json.load(data)['response']['docs']
    name = ""
    print(tweets[0]['user.screen_name'][0])
    if len(tweets) >0:
        name = tweets[0]['user.screen_name'][0]
    return render(request, 'dashboard/result.html', {'tweets': tweets , 'name': name,'search_term':q,'selected_lang':language,'selected_country':country,'language':["Choose..","English","Hindi","Portugese"],'Country':["Choose..","India","USA","Brazil"]})


