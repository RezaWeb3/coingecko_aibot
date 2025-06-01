import requests
from dotenv import load_dotenv
import os
import datetime
from polygon import RESTClient 
from polygon.rest.models import (TickerNews,)


class StockNews:
    def __init__(self):
        api_key = os.getenv('POLYGON_API')
        if api_key:
            print(f"POLYGON API Key exists and begins {api_key[:8]}")
        else:
            print("POLYGON API Key not set")
            return
        self.API_KEY = api_key
        self.client = RESTClient(api_key)

    def getSMAs(self, symbol, startingdate_str, endingdate_str):
        sma = self.client.get_sma(
            ticker=symbol,
            timestamp_gte=startingdate_str,
            timestamp_lte=endingdate_str,
            timespan="day",
            adjusted="true",
            window="1",
            series_type="close",
            order="desc",
        )
        print("inside2")
        print(sma)
        return sma
    
    def getNews (self, symbol, startingdatestr, endingdatestr):
        news = []
        for n in self.client.list_ticker_news(
            ticker=symbol,
            published_utc_gte=startingdatestr,
            published_utc_lte=endingdatestr,
            order="asc",
            limit="10",
            sort="published_utc",
            ):
            news.append(n)
        return news
        #print(news)

    def searchNewsPrice(self, symbol, pricestartingdate, priceendingdate, newsstartingdate, newsendingdate):
        SMAs=[]
        dates=[]
        news = []
        response_stockperf = self.getSMAs(symbol, pricestartingdate, priceendingdate)
        SMA_dates = []
        for result in response_stockperf.values:
            print(result)
            timestamp, value = result.timestamp, result.value
            SMA_dates.append({"sma":value, "date":datetime.datetime.fromtimestamp(float(timestamp/1000)).date().strftime("%Y-%m-%d")})
        
        results = self.getNews(symbol, newsstartingdate, newsendingdate)
        articles = []
        print(results)
        for index, item in enumerate(results):
            # verify this is an agg
            dt = datetime.datetime.strptime(item.published_utc, "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.replace(tzinfo=datetime.timezone.utc).date().strftime("%Y-%m-%d")
            title = item.title
            publisher = item.publisher.name
            author = item.author
            desc = item.description
            sentimentobj = [{"sentiment": insight.sentiment, "reason": insight.sentiment_reasoning } for insight in item.insights if insight.ticker == symbol]
            reason = None# item.insights.senstiment_reasoning
            
            articles.append({"date":dt, 
                            "title":title,
                            "publisher": publisher,
                            "author":author,
                            "description":desc,
                            "sentiment":sentimentobj[0]["sentiment"],
                            "reason":sentimentobj[0]["reason"]
                            })
        
            if index == 20:
                break
    


        return {"articles": articles, "SMAs": SMA_dates}
        
