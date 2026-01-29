from fastapi import FastAPI
import feedparser
import trafilatura
from dateutil import parser as date_parser
from datetime import datetime, timezone

app = FastAPI()

FEEDS = {
    "FOX": "https://moxie.foxnews.com/google-publisher/politics.xml",
    "GUARDIAN": "https://www.theguardian.com/us-news/politics/rss", 
    "NYT": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", 
    "HUFFPOST": "https://www.huffpost.com/section/politics/feed"
}

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

@app.get("/")
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



# TO-DO LIST:

# MAKE NYC WORK
# MAKE CNN WORK?
# CONNECT TO TWITTER
# CONNECT TO AI