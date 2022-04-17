import requests
from django.shortcuts import render
import _json

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from .forms import NameForm

# Create your views here.
def homepage(request):
    #send api request
    word = "https://random-word-api.herokuapp.com/word"
    response = requests.get(word)

    #get api response for random word
    json_ = response.json()
    wordOfDay = json_[0]

    #get api request url for dictionary
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    key = "?key=d7045d21-8d0c-4c61-9aea-8321bb66b12e"
    url += word + key

    #get json file from api
    websterResponse = requests.get(url)
    wordJson = websterResponse.json()

    #get definition for random word
    for i in range(len((wordJson[0])['def'])):
        definition = (    ((((((((wordJson[0]['def'])[i])['sseq'])[0])[0])[1])['dt'])[0])[1]   )
    definition = definition[4:]

    #send to front end
    return render(request, 'homepage.html', {"word" : word, "definition": definition})

def wordpage(request, word):
    #get api request url
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    key = "?key=d7045d21-8d0c-4c61-9aea-8321bb66b12e"
    url += word + key

    #get json file from api
    response = requests.get(url)
    wordJson = response.json()

    definition =   ((((((wordJson[0]['def'])[0])['sseq'])[0])[0])[0])
    if (definition == "pseq"):
        definition = (((((((wordJson[0]['def'])[0])['sseq'])[0])[0])[1])[0][1])['dt'][0][1]
    else:
        definition = (    ((((((((wordJson[0]['def'])[0])['sseq'])[0])[0])[1])['dt'])[0])[1]   )
    definition = definition[4:]

    definition = definition.replace("{it}","")
    definition = definition.replace("{/it}","")

    while (definition.find("{d_link|") != -1):
        definition = definition.replace("{d_link|","",1)
        removeStart = definition.find("|")
        removeEnd = definition.find("}", removeStart)
        definition = definition[0:removeStart] + definition[removeEnd + 1:]

    #send to front end
    return render(request, 'wordpage.html', {"word" : word, "definition": definition})

def get_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            wordSearch = form.cleaned_data['searchbar']
            # redirect to a new URL:
            return HttpResponseRedirect('/' + wordSearch)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'wordpage.html', wordSearch, {'form': form})