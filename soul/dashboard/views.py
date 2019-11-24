from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from urllib.parse import quote
from collections import Counter
from dateutil import parser
import operator

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
    langdict={'en':'English','hi':'Hindi','pt':'Portugese','nl':"Dutch","es":"Spanish","fr":"French","sv":"Swedish","und":"Undefined"}
    for code, value in langdict.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        if language == value:
            lang=code
            break
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
    url = 'http://18.223.109.186:8983/solr/IRF19P1/select?q=(text_en%3A('+q+')%20OR%20'+'text_hi%3A('+q+')%20OR%20'+'text_pt%3A('+q+')%20OR%20'+'full_text%3A('+q+'))'+lang_filter+country_filter+'&wt=json&indent=true&rows=10000'
    data = urlopen(url)
    tweets = json.load(data)['response']['docs']
    cnt = Counter()
    cnt1 = Counter()
    cnt2 = Counter()
    cnt3 = Counter()
    cnt4 = {"India":Counter(),"USA":Counter(),"Brazil":Counter()}
    for d in tweets:
        v1 = d['country'][0]
        v2 = d['lang'][0]
        if 'hashtags' in d:
            for v3 in d['hashtags']:
                cnt3[v3]+=1
        v4=str(parser.parse(d['tweet_date'][0]).date())
        if v1=="India": cnt4["India"][v4]+=1 
        else: cnt4["India"][v4]+=0
        if v1=="USA": cnt4["USA"][v4]+=1  
        else: cnt4["USA"][v4]+=0
        if v1=="Brazil": cnt4["Brazil"][v4]+=1 
        else: cnt4["Brazil"][v4]+=0
        cnt1[v1]+=1
        cnt2[v2]+=1
    tweetcount = list(cnt1.values())
    print("Tweetcount",tweetcount)
    langcount = list(cnt2.values())
    print("Langcount",langcount)
    countries = list(cnt1.keys())
    print("Countries",countries)
    languages = list(cnt2.keys())
    print("Languages",languages)
    for i in range(len(languages)):
        languages[i]=langdict[languages[i]]
    t = sorted(cnt3.items(), key=lambda x:-x[1])[:10]
    hashtagcount=[b for a,b in t]
    hashtags=[a for a,b in t]
    print(hashtagcount)
    print(hashtags)
    k1=sorted(cnt4["India"].items(), key=operator.itemgetter(0))
    k2=sorted(cnt4["USA"].items(), key=operator.itemgetter(0))
    k3=sorted(cnt4["Brazil"].items(), key=operator.itemgetter(0))
    print(k1)
    print(k2)
    print(k3)
    tweetdatecount={}
    tweetdates=[a for a,b in k1]
    tweetdatecount["India"]=[b for a,b in k1]
    tweetdatecount["USA"]=[b for a,b in k2]
    tweetdatecount["Brazil"]=[b for a,b in k3]
    name = ""
    print(tweets[0]['user.screen_name'][0])
    if len(tweets) >0:
        name = tweets[0]['user.screen_name'][0]
    my_dict={'tweets': tweets , 'name': name,'search_term':q,'selected_lang':language,'selected_country':country,'language':["Choose..","English","Hindi","Portugese"],
    'Country':["Choose..","India","USA","Brazil"],'countries':countries,
    'tweetcount':tweetcount,"langs":languages,
    "langcount":langcount,"trendhashtags":hashtags,
    "trendhashcounts":hashtagcount,"tweetdates":tweetdates,"india_tweetdatecount":tweetdatecount["India"],
   "usa_tweetdatecount":tweetdatecount["USA"],"brazil_tweetdatecount":tweetdatecount["Brazil"] }
    return render(request, 'dashboard/result.html', my_dict)


