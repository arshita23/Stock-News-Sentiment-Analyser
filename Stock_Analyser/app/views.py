from django.shortcuts import render, HttpResponse
from .models import New

import nltk
nltk.download('vader_lexicon')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from newsapi import NewsApiClient
from datetime import date, timedelta, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

pd.set_option('display.max_colwidth',1000)

NEWS_API_KEY = "f49400abecf94e12887066996c925a07"

newsapi = NewsApiClient(api_key = NEWS_API_KEY)



def index(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = New.objects.filter(email = email).first()
        if data:
            if (password == data.password):
                return render(request,"homepage.html")
                
            else:
                return render(request, "login.html",{"error_message": "password is incorrect"})
        else:
            return render(request, "login.html",{"error_message": "user not found"})
    return render(request,"login.html")
# Create your views here.



# def homePage(request):
#         # if request.method =="GET":
#         #     return render(request, "home.html")
        
#         # if request.method =="POST":
#         #     return render(request, "home.html")
        
        
#         if request.method == "POST":
#             search = request.POST.get('search')
#             if search:
#                 return render(request, "home.html")
            
