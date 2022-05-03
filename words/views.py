from multiprocessing import context
import requests
from django.shortcuts import render
import _json
import string

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from .forms import NameForm

# Create your views here.
def homepage(request):
    #send api request
    url = "https://random-word-api.herokuapp.com/word"
    response = requests.get(url)


    #get api response for random word
    json_ = response.json()
    wordOfDay = json_[0]

   #WORDS API DEFINITION
    url = "https://wordsapiv1.p.rapidapi.com/words/"
    url += wordOfDay + "/definitions"

    headers = {
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
        "X-RapidAPI-Key": "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa"
    }

    formalDefList = []

    #error handling
    try:
        response = requests.request("GET", url, headers=headers)
        wordJson = response.json()
        i = 1
        formalText = ""
        for d in (wordJson['definitions']):
            if (i == 4):
                break
            x = str(i) + ": " + str(d['definition'])
            formalDefList.append(x)
            i += 1
            formalText += "formal definition" + x 
    except:
        return render(request, "notword.html")

    while(len(formalDefList) == 0):
        url = "https://random-word-api.herokuapp.com/word"
        response = requests.get(url)

        #get api response for random word
        json_ = response.json()
        wordOfDay = json_[0]

        #WORDS API DEFINITION
        url = "https://wordsapiv1.p.rapidapi.com/words/"
        url += wordOfDay + "/definitions"

        headers = {
            "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
            "X-RapidAPI-Key": "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa"
        }

        formalDefList = []

        #error handling
        response = requests.request("GET", url, headers=headers)
        wordJson = response.json()
        i = 1
        formalText = ""
        for d in (wordJson['definitions']):
            if (i == 4):
                break
            x = str(i) + ": " + str(d['definition'])
            formalDefList.append(x)
            i += 1
            formalText += "formal definition" + x 
    

    


    #Urban Dictionary API Dictionary

    #Send API request and get response
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": wordOfDay}
    headers = {
    'x-rapidapi-key': "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa",
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }   

    response = requests.request("GET", url, headers=headers, params=querystring)
    wordJson = response.json()


    #Parse through json and clean up
    slangDefList = []
    i = 1
    slangText = ""
    for slangDef in (wordJson['list']):
        if (i==4):
            break
        x = str(i) + ": " + str(slangDef['definition'])
        x = x.replace("[", "")
        x = x.replace("]", "")
        slangDefList.append(x)
        i += 1
        slangText += "slang definition" + x

    if len(slangDefList) == 0:
        slangDefList.append("No Slang Definitions Found")

    #define the dictionary to front end
    wordOfDay.capitalize()
    context = {
        "word" : wordOfDay,
        "Formal" : formalDefList,
        "slangDef" : slangDefList,
        "formalText" : formalText,
        "slangText"  : slangText
    }

    #send to front end
    return render(request, 'homepage.html', context)

def wordpage(request, word):
    #WORDS API DEFINITION
    url = "https://wordsapiv1.p.rapidapi.com/words/"
    url += word + "/definitions"

    headers = {
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
        "X-RapidAPI-Key": "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa"
    }

    formalDefList = []

    #error handling
    formalText = ""
    try:
        response = requests.request("GET", url, headers=headers)
        wordJson = response.json()
        i = 1
        for d in (wordJson['definitions']):
            if (i == 4):
                break
            x = str(i) + ": " + str(d['definition'])
            formalDefList.append(x)
            i += 1
            formalText += "formal definition" + x 
    except:
        return render(request, "notword.html")



    #Urban Dictionary API Dictionary

    #Send API request and get response
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": word}
    headers = {
    'x-rapidapi-key': "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa",
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }   

    response = requests.request("GET", url, headers=headers, params=querystring)
    wordJson = response.json()


    #Parse through json and clean up
    slangDefList = []
    slangText = ""
    i = 1
    for slangDef in (wordJson['list']):
        if (i==4):
            break
        x = str(i) + ": " + str(slangDef['definition'])
        x = x.replace("[", "")
        x = x.replace("]", "")
        slangDefList.append(x)
        i += 1
        slangText += "slang definition" + x
        
    #Pronunciation
    try:
        #get word pronuciation
        url = "https://wordsapiv1.p.rapidapi.com/words/"
        url += word + "/pronunciation"

        headers = {
            "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
            "X-RapidAPI-Key": "bdf46a7a41msh7340c999b57f051p1cdf9cjsn032baa9651fa"
        }

        response = requests.request("GET", url, headers=headers)
        wordJson = response.json()
        pronuc = "(" + wordJson["pronunciation"]["all"] + ")"
    except:
        pronuc = ""

    #Error Handling for Text-to-speech
    if (formalText == ""):
        formalText = "No Formal Definition Found"
    if (slangText == ""):
        slangText = "No Slang Definition Found"

    if len(slangDefList) == 0:
        slangDefList.append("No Slang Definitions Found")
    if len(formalDefList) == 0:
        formalDefList.append("No Formal Definitons Found")
        
    #define the dictionary to front end
    word.capitalize()
    context = {
        "word" : word,
        "Formal" : formalDefList,
        "slangDef" : slangDefList,
        "formalText" : formalText,
        "slangText"  : slangText, 
        "pro" : pronuc
    }

    #send to front end
    return render(request, 'wordpage.html', context)

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
        else:
            return render(request, 'notword.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'wordpage.html', wordSearch, {'form': form})