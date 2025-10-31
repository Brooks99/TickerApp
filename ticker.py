import tkinter as tk
from yfinance import Ticker
import feedparser  # Add this import for RSS feeds
import ssl
import certifi
import json
import os
import pandas_market_calendars as mcal
from datetime import datetime
import pytz

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

class StockTicker:
    def __init__(self):
        self.config = self.load_config()
        self.root = tk.Tk()
        self.root.title("Tickrly")
        self.canvas = None
        self.update_button = None
        self._stocks = {}
        self._last_prices = {}
        self.scroll_position = 0
        self.canvas_width = self.config['canvas']['width']
        self.news_scroll_position = 0
        self.news_items = []
        self.news_canvas = None
        self.news_height = self.config['canvas']['news_height']
        
        
    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        return {
            "canvas": {
                "width": 800,
                "stock_height": 40,
                "news_height": 40
            },
            "display": {
                "stock_font_size": 16,
                "news_font_size": 12,
                "stock_spacing": 20,
                "news_spacing": 40,
                "scroll_speed": 2
            },
            "updates": {
                "interval": 60000  # Update interval in milliseconds (1 minute)
            },
            "stocks": {
                "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "JOBY"]
            }
        }

    def initialize_stocks(self):
        """Initialize stocks from config"""
        for symbol in self.config['stocks']['symbols']:
            self._stocks[symbol] = {
                'display_text': f"{symbol} | Loading...",
                'color': 'white',
                'arrow': ''
            }
            self._last_prices[symbol] = 0

    def _handle_missing_data(self, ticker):
        """Handle cases where stock data cannot be retrieved"""
        self._stocks[ticker] = {
            'display_text': f"{ticker} | Data Unavailable",
            'color': 'gray',
            'arrow': ''
        }
        self._last_prices[ticker] = 0
        
    def update_title(self):
        try:
            # Update the window title with the current date and time
            # Check market status
            is_open, status = self.is_market_open()
            if not is_open:
                # If market is closed, set title accordingly
                self.root.title("Tickrly - {status}")
            else:
                self.root.title("Tickrly")    
        except Exception as e:
            print(f"Error updating window title: {e}")
                 

    def update_stock(self, ticker):
        try:
            stock = Ticker(ticker)
            # Get both open and current prices
            info = stock.history(period='1d')
            if info.empty:
                self._handle_missing_data(ticker)
                return
            
            open_price = info['Open'].iloc[0]  # Get the opening price
            current_price = stock.info.get('regularMarketPrice', info['Close'].iloc[-1])  # Get current price or latest close
            diff_price = current_price - open_price
            
            display_text = f"{ticker} | Open: ${open_price:.2f} Current Diff: ${diff_price:.2f}"
            color = 'white'
            
            if current_price < open_price:
                arrow = "▼"
                color = 'red'
            elif current_price > open_price:
                arrow = "▲"
                color = 'green'
            else:
                arrow = ""
                
            self._stocks[ticker] = {
                'display_text': display_text,
                'color': color,
                'arrow': arrow
            }
            self._last_prices[ticker] = current_price
            
        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            self._handle_missing_data(ticker)

    def update_news(self):
        try:
            # Using alternative Yahoo Finance RSS feed
            feed_url = "http://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US"
            
            # Add headers to mimic a browser request
            import urllib.request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            req = urllib.request.Request(feed_url, headers=headers)
            
            # Parse feed with error handling
            try:
                feed = feedparser.parse(urllib.request.urlopen(req))
            except urllib.error.URLError as e:
                print(f"SSL Error: {e}")
                # Try alternative feed URL
                feed_url = "https://finance.yahoo.com/news/rssindex"
                req = urllib.request.Request(feed_url, headers=headers)
                feed = feedparser.parse(urllib.request.urlopen(req))
            
            self.news_items = []
            
            if (feed.entries):
                for entry in feed.entries[:6]:  # Get first 6 news items
                    title = entry.get('title', 'No title available')
                    link = entry.get('link', '#')
                    self.news_items.append({
                        'text': f"📰 {title}",
                        'color': 'yellow',
                        'link': link
                    })
            else:
                raise Exception("No news entries found")
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            self.news_items = [{'text': '📰 Unable to fetch news', 'color': 'red'}]

    def create_canvas(self):
        # Create stock ticker canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=self.config['canvas']['width'], 
            height=self.config['canvas']['stock_height'], 
            bg='black'
        )
        self.canvas.pack(fill='x', expand=False, pady=(0, 0))  # Add 10 pixels padding below
        
        # Create news ticker canvas
        self.news_canvas = tk.Canvas(
            self.root, 
            width=self.config['canvas']['width'], 
            height=self.config['canvas']['news_height'], 
            bg='black'
        )
        self.news_canvas.pack(fill='x', expand=False)

    def update_all_stocks(self):
        """Update all stocks from config symbols"""
        for ticker in self.config['stocks']['symbols']:
            self.update_stock(ticker)

    def draw_stocks(self):
        if not self.canvas:
            return
            
        self.canvas.delete('all')
        
        spacing = self.config['display']['stock_spacing']
        x_position = self.canvas_width - self.scroll_position
        y_position = self.config['canvas']['stock_height'] // 2
        
        # Calculate total width of all tickers
        total_width = sum(len(data['display_text'] + data['arrow']) * 10 + spacing 
                         for data in self._stocks.values())
        
        # Draw stocks multiple times to ensure continuous scrolling
        for offset in [-total_width, 0, total_width]:
            current_x = x_position + offset
            for symbol, data in self._stocks.items():
                text = f"{data['display_text']}{data['arrow']}"
                self.canvas.create_text(
                    current_x, y_position,
                    anchor='w',
                    font=('Arial', self.config['display']['stock_font_size'], 'bold'),
                    fill=data['color'],
                    text=text
                )
                current_x += len(text) * 10 + spacing

    def draw_news(self):
        if not self.news_canvas or not self.news_items:
            return
            
        self.news_canvas.delete('all')
        
        spacing = 40
        x_position = self.canvas_width - self.news_scroll_position
        y_position = self.news_height // 2
        
        # Join all news items with spacing
        news_text = "     |||     ".join(item['text'] for item in self.news_items)
        total_width = len(news_text) * 10
        
        # Draw news text multiple times for continuous scroll
        for offset in [-total_width, 0, total_width]:
            self.news_canvas.create_text(
                x_position + offset, y_position,
                anchor='w',
                font=('Arial', self.config['display']['news_font_size'], 'bold'),  # Use the configured font size for news
                fill='yellow',
                text=news_text
            )

    def animate(self):
        # Use fixed speed from config
        speed = self.config['display']['scroll_speed']
        self.scroll_position += speed
        
        # News ticker animation
        self.news_scroll_position += speed * 0.7  # Slightly slower than stocks
        
        # Calculate widths for wrapping
        stock_width = sum(len(data['display_text'] + data['arrow']) * 10 + 20 
                         for data in self._stocks.values())
        news_width = len("     |||     ".join(item['text'] 
                        for item in self.news_items)) * 10
        
        # Wrap positions
        if self.scroll_position >= stock_width:
            self.scroll_position -= stock_width
        if self.news_scroll_position >= news_width:
            self.news_scroll_position -= news_width
        
        self.draw_stocks()
        self.draw_news()
        self.root.after(16, self.animate)

    def schedule_updates(self):
        """Schedule periodic updates for stocks and news"""
        self.update_all_stocks()
        self.update_news()
        update_interval = self.config['updates']['interval']
        self.root.after(update_interval, self.schedule_updates)

    def is_market_open(self):
        """Check if the US stock market is currently open"""
        try:
            # Get NYSE calendar
            nyse = mcal.get_calendar('NYSE')
            
            # Get current time in ET (Eastern Time)
            et_tz = pytz.timezone('US/Eastern')
            current_time = datetime.now(et_tz)
            
            # Get market schedule for today
            schedule = nyse.schedule(
                start_date=current_time.date(),
                end_date=current_time.date()
            )
            
            if schedule.empty:
                return False, "Market Closed (Weekend - Holiday)"
                
            market_open = schedule.iloc[0]['market_open'].tz_convert(et_tz)
            market_close = schedule.iloc[0]['market_close'].tz_convert(et_tz)
            
            if market_open <= current_time <= market_close:
                return True, "Market Open"
            elif current_time < market_open:
                return False, f"Market Opens at {market_open.strftime('%I:%M %p ET')}"
            else:
                return False, "Market Closed"
                
        except Exception as e:
            print(f"Error checking market status: {e}")
            return False, "Market Status Unknown"

def main():
    app = StockTicker()
    
    #app.initialize_stocks
    
    app.create_canvas()
    
    # Update the title initially    
    app.update_title()
    
    # Initialize stocks first
    app.initialize_stocks()
    
    # Initial updates
    app.update_all_stocks()
    app.update_news()
    
    # Start periodic updates
    app.schedule_updates()
    
    # Start animation
    app.animate()
    app.root.mainloop()

if __name__ == "__main__":
    print("hello")
    main()
    