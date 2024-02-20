from django.shortcuts import render, HttpResponse, redirect
from .models import New
from credentials import views
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django.contrib.auth.hashers import make_password,check_password
# print(make_password('1234'))
# print("cool")
import nltk
nltk.download('vader_lexicon')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from newsapi import NewsApiClient
from datetime import date, timedelta, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

pd.set_option('display.max_colwidth',1100)

NEWS_API_KEY = "f49400abecf94e12887066996c925a07"

newsapi = NewsApiClient(api_key = NEWS_API_KEY)

# from Stock_Analyser.views import session_login_required


from functools import wraps

def session_login_required(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def f(request, *args, **kwargs):
            token = request.session.get('token', False)

            if token:
                access_token = AccessToken(token)
                print(access_token)
                user = access_token.payload.get('user_id')
                print(user)
                return view_func(request, *args, **kwargs)
            
            return redirect('/')
        
        return f
    if function is not None:
        return decorator(function)
    return decorator

def index(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if 'token' in request.session: 
                
                return render(request, "homepage.html")
            user = New.objects.get(email=email)

        # data = New.objects.filter(email = email).first()
        
            if user is not None:
                if check_password(password,user.password):
                    refresh= RefreshToken.for_user(user)
                    token=str(refresh.access_token)
                    request.session['token']=token
                else:
                    return render(request, "login.html",{"error_message": "Password is Incorrect"})                    

            else: 
                return render(request, "login.html",{"error_message": "User Not Found"}) 
            
        except Exception as e:
            print(e)


        #     if check_password(password,data.password):
        #     # if data:
        #     # if (password == data.password):
        #         return render(request,"homepage.html")
        #     else:
        #         return render(request, "login.html",{"error_message": "Password is Incorrect"})
        # else:
        #     return render(request, "login.html",{"error_message": "User Not Found"})
    return render(request,"login.html")
# Create your views here.

@session_login_required
def get_news(request):
    if request.method == "POST":
        company = request.POST.get('company')
        keywrd= company+" stock"
        s1 = datetime.now().date()
        startd = s1 - timedelta(days=5)
        newsapi = NewsApiClient(api_key = NEWS_API_KEY)
        
        if type(startd) == str:
            my_date = datetime.strptime(startd, '%d-%b-%Y')

        else:
            my_date = startd

        articles = newsapi.get_everything(q = keywrd,
                                        from_param = my_date.isoformat(),
                                        to = (my_date + timedelta(days = 2)).isoformat(),
                                        language = "en",
                                        sort_by = "relevancy",
                                        page_size = 100)
    
        articles_list = articles['articles']
        if not articles_list:
            error_message = "No Stock News found for {}".format(company)
            return render(request,"homepage.html", {"error_message": error_message})
        articles_list = sorted(articles_list, key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
        date_sentiments = {}
        date_sentiments_list = []
        seen = set()

        for article in articles_list:
            if str(article['title']) in seen:
                continue
            else:
                seen.add(str(article['title']))
                article_content = str(article['title']) + '. ' + str(article['description'])
                sentiment = sia.polarity_scores(article_content)['compound']
                date_sentiments.setdefault(my_date, []).append(sentiment)
                published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
                date_sentiments_list.append((article['title'],sentiment,published_at))
        date_sentiments_l = sorted(date_sentiments_list, key=lambda tup: tup[0],reverse = True)
        sent_list = list(date_sentiments.values())[0]
        stock_data = pd.DataFrame(date_sentiments_list, columns=['Headline', 'Sentiment', 'PublishedAt'])
        def replace_sentiment(sentiment):
            if sentiment < 0:
                return 'Negative'
            elif sentiment >0:
                return 'Positive'
            else:
                return sentiment
        stock_data=stock_data[stock_data['Sentiment']!=0]
        stock_data=stock_data.reset_index(drop=True)
        stock_data['Sentiment'] = stock_data['Sentiment'].apply(replace_sentiment)
        stock_data_html=stock_data.to_html(index = False)
        stock_data_html = stock_data_html.replace('<th>', '<th style="text-align: center;">')
        return render(request,"homepage.html",{"company_name":company,"stock_data_html":stock_data_html})
    return render(request,"homepage.html")


def logout_user(request):
    del request.session['token']
    return redirect('/')


# def homePage(request):
#         # if request.method =="GET":
#         #     return render(request, "home.html")
        
#         # if request.method =="POST":
#         #     return render(request, "home.html")
        
        
#         if request.method == "POST":
#             search = request.POST.get('search')
#             if search:
#                 return render(request, "home.html")
        
