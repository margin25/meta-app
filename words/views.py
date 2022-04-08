import requests
from django.shortcuts import render
import _json

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', {})

def wordpage(request, word):
    #get api request url
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    key = "?key=d7045d21-8d0c-4c61-9aea-8321bb66b12e"
    url += word + key

    #get json file from api
    response = requests.get(url)
    wordJson = response.json()

    #get definition
    for i in range(len((wordJson[0])['def'])):
        definition = (    ((((((((wordJson[0]['def'])[i])['sseq'])[0])[0])[1])['dt'])[0])[1]   )

    definition = definition[4:]
    return render(request, 'wordpage.html', {"word" : word, "definition": definition})
