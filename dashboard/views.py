from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from collections import defaultdict
from urllib.parse import quote
from collections import Counter
from dateutil import parser
import operator
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
# Create your views here.

'''
def home(request):
    return HttpResponse('<h1>SOUL</h1>')
'''


def home(request):
    return render(request, 'dashboard/dashboard.html', {'name': 'Goutham','search_term':"search",'language':["English","Hindi","Portugese"],'Country':["India","USA","Brazil"]})


search = ""
lang = ""
cout = ""


def getData(request):

    try:
        searchText = request.GET['q']
        language = request.GET['language']
        country = request.GET['country']
        search = searchText
        lang = language
        cout = country
    except MultiValueDictKeyError:
        searchText = search
        language = lang
        country = cout
    q = quote(searchText)
    language=quote(language)
    langdict = defaultdict(lambda : 'undefined')
    langdict.update({
        'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek',
        'es': 'Spanish', 'fa': 'Persian','fi':'Finnish','fil':'Filipino','fr':'French','he':'Hebrew','hi':'Hindi','hu':'Hungarian','id':'Indonesian','it':'Italian','ja':'Japanese','ko':'Korean','msa':'Malay','nl':'Dutch','no':'Norwegian','pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian','sv':'Swedish','th':'Thai','tr':'Turkish','uk':'Ukrainian','ur':'Urdu','vi':'Vietnamese','zh-cn':'Chinese','zh-tw':'Chinese',"und":"Undefined","in":"Hindi"
    })

    #langdict= {'en':'English','ar':'Arabic','bn':'Bengali','cs':'Czech','da':'Danish','de':'German','el':'Greek','es':'Spanish','fa':'Persian','fi':'Finnish','fil':'Filipino','fr':'French','he':'Hebrew','hi':'Hindi','hu':'Hungarian','id':'Indonesian','it':'Italian','ja':'Japanese','ko':'Korean','msa':'Malay','nl':'Dutch','no':'Norwegian','pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian','sv':'Swedish','th':'Thai','tr':'Turkish','uk':'Ukrainian','ur':'Urdu','vi':'Vietnamese','zh-cn':'Chinese','zh-tw':'Chinese',"und":"Undefined","in":"Hindi"}
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
    url = 'http://18.223.109.186:8983/solr/IRF19P1/select?q=(text_en%3A('+q+')%20OR%20'+'text_hi%3A('+q+')%20OR%20'+'text_pt%3A('+q+')%20OR%20'+'full_text%3A('+q+'))'+lang_filter+country_filter+'&wt=json&indent=true&rows=500'
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

    langcount = list(cnt2.values())

    countries = list(cnt1.keys())

    languages = list(cnt2.keys())

    for i in range(len(languages)):
        languages[i]=langdict[languages[i]]
    t = sorted(cnt3.items(), key=lambda x:-x[1])[:10]
    hashtagcount=[b for a,b in t]
    hashtags=[a for a,b in t]

    k1=sorted(cnt4["India"].items(), key=operator.itemgetter(0))
    k2=sorted(cnt4["USA"].items(), key=operator.itemgetter(0))
    k3=sorted(cnt4["Brazil"].items(), key=operator.itemgetter(0))

    tweetdatecount={}
    tweetdates=[a for a,b in k1]
    tweetdatecount["India"]=[b for a,b in k1]
    tweetdatecount["USA"]=[b for a,b in k2]
    tweetdatecount["Brazil"]=[b for a,b in k3]
    name = ""

    if len(tweets) >0:
        name = tweets[0]['user.screen_name'][0]

        paginator = Paginator(tweets, 20)
        page = request.GET.get('page')
        paginateTweets = paginator.get_page(page)
    my_dict={'tweets': tweets , 'name': name,'search_term':q,'selected_lang':language,'selected_country':country,'language':["Choose..","English","Hindi","Portugese"],
    'Country':["Choose..","India","USA","Brazil"],'countries':countries,
    'tweetcount':tweetcount,"langs":languages,
    "langcount":langcount,"trendhashtags":hashtags,
    "trendhashcounts":hashtagcount,"tweetdates":tweetdates,"india_tweetdatecount":tweetdatecount["India"],
   "usa_tweetdatecount":tweetdatecount["USA"],"brazil_tweetdatecount":tweetdatecount["Brazil"], 'paginateTweets':paginateTweets }
    return render(request, 'dashboard/result.html', my_dict)


