# Polymarket News Scraper Bot
A real-time news aggregator designed to find market-moving political news 
from Fox, The Guardian, Twitter and other sources for prediction markets.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Start the bot: `uvicorn main:app --reload`
3. Open `http://127.0.0.1:8000` to see the live feed.