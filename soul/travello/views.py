from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
'''
def home(request):
    return HttpResponse('<h1>SOUL</h1>')
'''

def index(request):
    return render(request,'travello/index.html', {'price': 700})