🤖 PolyMarket-AI News Bot

A real-time news aggregator and parser designed to find market-moving political news for prediction markets like Polymarket.

🚀 Features

Multi-Source Scraping: Fetches data from Fox News, The Guardian, and more.
Smart Filtering: Uses `trafilatura` for high-accuracy text extraction (bypassing common bot blocks).
UTC-Standardized: All article times are normalized to UTC for accurate betting window analysis.
Clean Data: Automatically filters out "ghost" data and legacy RSS entries.

uvicorn main:app --reload
