from fastapi import FastAPI
import feedparser
import trafilatura
from dateutil import parser as date_parser
from datetime import datetime, timezone
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")

app = FastAPI()

FEEDS = {
    "FOX": "https://moxie.foxnews.com/google-publisher/politics.xml",
    "GUARDIAN": "https://www.theguardian.com/us-news/politics/rss", 
    "HUFFPOST": "https://www.huffpost.com/section/politics/feed"
}

TWEETER_ACCOUNTS ={
    "WhiteHouse",
    "elonmusk",
    "CNN",
    "nytimes",
    "Europarl_EN"
}

def get_latest_tweets():
    all_tweets = []
    url = "https://api.twitterapi.io/twitter/user/last_tweets"
    headers = {"X-API-Key": TWITTER_API_KEY}

    for account in TWEETER_ACCOUNTS:
        params = {"userName": account, "includeReplies": True}

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                tweets_data = json_data.get("data", {}).get("tweets", [])
                
                for t in tweets_data[:10]:
                    all_tweets.append({
                        "author": account,
                        "text": t.get("text"),
                        "created_at": get_utc_time(t.get("createdAt")),
                        "link": t.get("url")
                    })

            time.sleep(5)
        except Exception as e:
            print(f"Error fetching {account}: {e}")
            
    return all_tweets



def get_utc_time(entry):
    date_str = getattr(entry, 'published', getattr(entry, 'pubDate', None))
    if not date_str: return datetime.now(timezone.utc)
    try:
        dt = date_parser.parse(date_str)
        return dt.astimezone(timezone.utc)
    except:
        return datetime.now(timezone.utc)

def scrape_article(url):
   
    try:
        downloaded = trafilatura.fetch_url(url)
        result = trafilatura.extract(downloaded)
        return result if result else "Text extraction failed (empty)"
    except Exception as e:
        return f"Scrape Error: {str(e)}"
    
def get_bot_data():
    results = []
    now = datetime.now(timezone.utc)
    
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            pub_date = get_utc_time(entry)
            age_delta = now - pub_date
            minutes_old = int(age_delta.total_seconds() / 60)

            results.append({
                "source": source,
                "title": entry.title,
                "published": getattr(entry, 'published', 'unknown'),
                "age_minutes": minutes_old,
                "full_text": scrape_article(entry.link),
                "link": entry.link
            })
            
    return {"bot_time_utc": now.isoformat(), "articles": results}

@app.get("/")
def get_pulse():
    news = get_bot_data() 
    tweets = get_latest_tweets()
    
    return {
        "news_articles": news,
        "tweets": tweets,
        "bot_time_utc": datetime.now(timezone.utc).isoformat()
    }




# TO-DO LIST:

# MAKE NYC WORK
# MAKE CNN WORK?
# CONNECT TO TWITTER
# CONNECT TO AI