import os
import sys
import locale
import logging

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure macOS localization falls back to en_US.UTF-8 so Tk won't produce nil menu titles
try:
    # Try to set the locale through the locale module first
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    logger.info("Locale set through locale module")
except Exception as e:
    logger.warning(f"Could not set locale through locale module: {e}")

# Ensure environment variables are set as a fallback
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
logger.info(f"Environment variables set: LANG={os.environ.get('LANG')}, LC_ALL={os.environ.get('LC_ALL')}")

# Force PyObjC bridge to initialize with UTF-8
if sys.platform == 'darwin':
    try:
        from Foundation import NSLocale
        preferredLang = NSLocale.preferredLanguages()[0]
        logger.info(f"macOS preferred language: {preferredLang}")
    except Exception as e:
        logger.warning(f"Could not initialize PyObjC bridge: {e}")

# then the rest of imports
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
import logging
from tkinter import messagebox

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# Basic logging for the application. In production this can be configured to
# write to a file or use a more advanced configuration.
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

class ConfigEditor:
    def __init__(self, ticker_app):
        self.ticker_app = ticker_app
        self.window = None
        
    def toggle(self):
        """Show or hide the config editor window"""
        if self.window:
            self.window.destroy()
            self.window = None
            return
            
        self.window = tk.Toplevel(self.ticker_app.root)
        self.window.title("Stock Symbol Editor")
        self.window.geometry("400x500")
        
        # Create listbox for symbols
        frame = tk.Frame(self.window)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Stock Symbols", font=("Helvetica", 14, "bold")).pack()
        
        # Create listbox with scrollbar
        listbox_frame = tk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(10,5))
        
        self.symbol_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
        self.symbol_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.symbol_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.symbol_listbox.yview)
        
        # Add current symbols to listbox
        for symbol in self.ticker_app.config["stocks"]["symbols"]:
            self.symbol_listbox.insert(tk.END, symbol)
            
        # Add entry and buttons
        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.symbol_entry = tk.Entry(entry_frame)
        self.symbol_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,5))
        
        tk.Button(entry_frame, text="Add", command=self.add_symbol).pack(side=tk.LEFT)
        
        # Delete button
        tk.Button(frame, text="Delete Selected", command=self.delete_symbol).pack(pady=5)
        
        # Save and Cancel buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="Save", command=self.save_changes).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, expand=True, padx=5)
        
        # About and License buttons
        info_frame = tk.Frame(frame)
        info_frame.pack(fill=tk.X)
        tk.Button(info_frame, text="About", command=self.show_about).pack(side=tk.LEFT, padx=5, pady=(6,0))
        tk.Button(info_frame, text="License", command=self.show_license).pack(side=tk.LEFT, padx=5, pady=(6,0))
        
    def add_symbol(self):
        """Add a new stock symbol"""
        symbol = self.symbol_entry.get().strip().upper()
        if symbol and symbol not in self.symbol_listbox.get(0, tk.END):
            self.symbol_listbox.insert(tk.END, symbol)
            self.symbol_entry.delete(0, tk.END)
            
    def delete_symbol(self):
        """Delete the selected symbol"""
        selection = self.symbol_listbox.curselection()
        if selection:
            self.symbol_listbox.delete(selection)
            
    def save_changes(self):
        """Save changes to config file and update the ticker"""
        symbols = list(self.symbol_listbox.get(0, tk.END))
        self.ticker_app.config["stocks"]["symbols"] = symbols
        
        # Save to config file
        config_path = self.ticker_app.get_config_path()
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(self.ticker_app.config, f, indent=4)
            
        # Update the ticker display
        self.ticker_app._stocks = {}  # Clear cached stock data
        self.ticker_app._last_prices = {}
        self.ticker_app._refresh_action()  # Refresh the display
        
        self.window.destroy()

    def show_about(self):
        """Show an About dialog with application information."""
        about_text = (
            "Tickrly\n"
            "Version: 1.0.2\n"
            "A lightweight stock and news ticker.\n\n"
            "Visit:  https://github.com/Brooks99/TickerApp for more information."
        )
        try:
            messagebox.showinfo("About Tickrly", about_text, parent=self.window)
        except Exception:
            # Fallback if parented messagebox fails
            messagebox.showinfo("About Tickrly", about_text)

    def show_license(self):
        """Show license text in a scrollable window. If a LICENSE file is present, show it."""
        license_win = tk.Toplevel(self.window)
        license_win.title("License")
        license_win.geometry("600x400")

        text_frame = tk.Frame(license_win)
        text_frame.pack(fill=tk.BOTH, expand=True)

        license_text = ""
        try:
            lic_path = os.path.join(os.path.dirname(__file__), 'LICENSE')
            if os.path.exists(lic_path):
                with open(lic_path, 'r') as f:
                    license_text = f.read()
            else:
                license_text = "No LICENSE file found. Please include a LICENSE in the project root."
        except Exception:
            license_text = "Unable to load license." 

        txt = tk.Text(text_frame, wrap='word')
        txt.insert('1.0', license_text)
        txt.config(state='disabled')
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scr = tk.Scrollbar(text_frame, command=txt.yview)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        txt['yscrollcommand'] = scr.set

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
        # Hover menu variables
        self.menu_frame = None
        self._menu_hide_after_id = None
        # Create hover menu and bindings
        self.create_hover_menu()
        
        # Initialize config editor
        self.config_editor = None
        # Bind click events to show config editor - only to main window
        self.root.bind("<Button-1>", self.handle_click)
        self.root.bind("<Double-Button-1>", self.handle_click)
        self.root.bind("<Configure>", lambda e: logger.debug(f"Configure: {e.width}, {e.height}"))
        
    def handle_click(self, event):
        """Handle click events to show/hide config editor"""
        if not self.config_editor:
            self.config_editor = ConfigEditor(self)
        self.config_editor.toggle()
        
    def get_config_path(self):
        """Get the path to the config file, preferring user's config directory"""
        # First, try user's config directory
        user_config_dir = os.path.expanduser('~/Library/Application Support/Tickrly')
        user_config_path = os.path.join(user_config_dir, 'config.json')
        
        # If user config exists, use it
        if os.path.exists(user_config_path):
            return user_config_path
            
        # If not, try the bundled config
        bundled_config = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(bundled_config):
            # Create user config directory if it doesn't exist
            os.makedirs(user_config_dir, exist_ok=True)
            # Copy bundled config to user directory
            import shutil
            shutil.copy2(bundled_config, user_config_path)
            return user_config_path
            
        # If neither exists, use user config path (will create default config)
        return user_config_path
    
    def load_config(self):
        config_path = self.get_config_path()
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default config
                default_config = {
                    "canvas": {"width": 1200, "stock_height": 40, "news_height": 40},
                    "stocks": {"symbols": ["^GSPC", "^DJI"]},
                    "display": {
                        "stock_font_size": 16,
                        "news_font_size": 16,
                        "stock_spacing": 20,
                        "news_spacing": 40,
                        "scroll_speed": 2
                    },
                    "updates": {"interval": 60000}
                }
                # Save default config
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            logger.exception("Error loading config")
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
        # Determine market status once at init
        try:
            is_open, status = self.is_market_open()
        except Exception:
            is_open = True

        for symbol in self.config['stocks']['symbols']:
            self._stocks[symbol] = {
                'display_text': f"{symbol} | Loading...",
                'color': 'white' if is_open else 'gray',
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
                self.root.title(f"Tickrly - {status} Click on stocks to edit")
            else:
                self.root.title("Tickrly")    
        except Exception as e:
            logger.exception("Error updating window title")
                 

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

            # If market is closed (or holiday), show neutral gray color
            try:
                if not getattr(self, 'market_is_open', True):
                    color = 'gray'
                    arrow = ''
            except Exception:
                pass
                
            self._stocks[ticker] = {
                'display_text': display_text,
                'color': color,
                'arrow': arrow
            }
            self._last_prices[ticker] = current_price
            
        except Exception as e:
            logger.exception("Error fetching stock data for %s", ticker)
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
                logger.warning("SSL/URL error while fetching news feed: %s", e)
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
            logger.exception("Error fetching news")
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

    def create_hover_menu(self):
        """Create a small menu that appears when the mouse hovers over the app window."""
        # Create the menu frame but do NOT map it yet; we'll show on hover
        self.menu_frame = tk.Frame(self.root, bg='#222222')

        # Buttons: Refresh, Toggle News, Settings (example actions)
        btn_style = {
            'bg': '#007AFF',        # macOS-style blue
            'fg': 'white',
            'activebackground': '#0051A8',
            'activeforeground': 'white',
            'relief': 'raised',
            'bd': 1,
            'highlightthickness': 0,
            'padx': 10,
            'pady': 6,
            'font': ('Helvetica', 11, 'bold')
        }

        refresh_btn = tk.Button(self.menu_frame, text='Refresh', command=self._refresh_action, **btn_style)
        toggle_news_btn = tk.Button(self.menu_frame, text='Toggle News', command=self._toggle_news_action, **btn_style)
        settings_btn = tk.Button(self.menu_frame, text='Settings', command=self._settings_action, **btn_style)

        # Pack the buttons into the menu frame
        refresh_btn.pack(side='left', padx=(8, 4), pady=6)
        toggle_news_btn.pack(side='left', padx=4, pady=6)
        settings_btn.pack(side='left', padx=4, pady=6)

        # Measure the menu height (used by hover detection) but don't show it yet
        self.menu_frame.update_idletasks()
        try:
            self.menu_height = self.menu_frame.winfo_reqheight()
        except Exception:
            self.menu_height = 40

        # Bind pointer motion and leave to control hover behavior across all widgets
        # use bind_all so motion events are captured even when over child widgets
        self.root.bind_all('<Motion>', self._on_motion)
        self.root.bind_all('<Leave>', self._on_root_leave)

    def _on_mouse_enter(self, event=None):
        # Cancel any scheduled hide and show immediately
        if self._menu_hide_after_id:
            try:
                self.root.after_cancel(self._menu_hide_after_id)
            except Exception:
                pass
            self._menu_hide_after_id = None
        self._show_menu()

    def _on_mouse_leave(self, event=None):
        # Schedule hiding the menu after a short delay to avoid flicker
        if self._menu_hide_after_id:
            try:
                self.root.after_cancel(self._menu_hide_after_id)
            except Exception:
                pass
        self._menu_hide_after_id = self.root.after(500, self._hide_menu)

    def _on_motion(self, event=None):
        """Show menu when mouse is near the top of the window; otherwise hide after delay."""
        try:
            root_y = self.root.winfo_rooty()
            rel_y = event.y_root - root_y
            # If mouse is within the top menu height (or slightly above), show
            if rel_y is not None and rel_y >= 0 and rel_y <= max(self.menu_height + 6, 40):
                if self._menu_hide_after_id:
                    try:
                        self.root.after_cancel(self._menu_hide_after_id)
                    except Exception:
                        pass
                    self._menu_hide_after_id = None
                self._show_menu()
            else:
                if self._menu_hide_after_id:
                    try:
                        self.root.after_cancel(self._menu_hide_after_id)
                    except Exception:
                        pass
                self._menu_hide_after_id = self.root.after(400, self._hide_menu)
        except Exception:
            pass

    def _on_root_leave(self, event=None):
        # Immediately hide when pointer leaves the toplevel area
        if self._menu_hide_after_id:
            try:
                self.root.after_cancel(self._menu_hide_after_id)
            except Exception:
                pass
        self._hide_menu()

    def _show_menu(self):
        if not self.menu_frame.winfo_ismapped():
            # Use place so showing/hiding doesn't change layout geometry
            self.menu_frame.place(x=0, y=0, relwidth=1)

    def _hide_menu(self):
        if self.menu_frame and self.menu_frame.winfo_ismapped():
            try:
                self.menu_frame.place_forget()
            except Exception:
                self.menu_frame.pack_forget()
        self._menu_hide_after_id = None

    def _refresh_action(self):
        # Manual refresh: update stocks and news immediately
        try:
            self.update_all_stocks()
            self.update_news()
        except Exception as e:
            logger.exception("Error during manual refresh")

    def _toggle_news_action(self):
        # Toggle visibility of the news canvas
        try:
            if self.news_canvas and self.news_canvas.winfo_ismapped():
                self.news_canvas.pack_forget()
            elif self.news_canvas:
                self.news_canvas.pack(fill='x', expand=False)
        except Exception as e:
            logger.exception("Error toggling news canvas")

    def _settings_action(self):
        # Open the config editor (settings) when the Settings button is clicked.
        try:
            if not self.config_editor:
                self.config_editor = ConfigEditor(self)
            # If window exists bring to front, otherwise create it
            if not (self.config_editor.window and self.config_editor.window.winfo_exists()):
                self.config_editor.toggle()
            else:
                try:
                    self.config_editor.window.lift()
                except Exception:
                    pass
        except Exception:
            logger.exception("Error opening settings/config editor")

    def update_all_stocks(self):
        """Update all stocks from config symbols"""
        # Check market status once per bulk update and store it
        try:
            is_open, status = self.is_market_open()
            self.market_is_open = is_open
            self.market_status = status
        except Exception:
            # If status check fails, assume open to avoid hiding information
            self.market_is_open = True
            self.market_status = 'Unknown'

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
            # We'll compare in UTC because the schedule timestamps are in UTC
            current_time_utc = datetime.now(pytz.utc)

            # Get today's date string in YYYY-MM-DD for the calendar
            et_tz = pytz.timezone('US/Eastern')
            today_et = datetime.now(et_tz).date()
            today_str = today_et.strftime('%Y-%m-%d')

            # Get market schedule for today
            schedule = nyse.schedule(
                start_date=today_str,
                end_date=today_str
            )
            
            if schedule.empty:
                return False, "Market Closed (Weekend - Holiday)"
                
            market_open = schedule.iloc[0]['market_open']
            market_close = schedule.iloc[0]['market_close']

            # Ensure market_open/close are timezone-aware (they should be)
            if market_open.tzinfo is None:
                market_open = market_open.tz_localize(pytz.utc)
            if market_close.tzinfo is None:
                market_close = market_close.tz_localize(pytz.utc)

            # Compare using UTC
            if market_open <= current_time_utc <= market_close:
                return True, "Market Open"
            elif current_time_utc < market_open:
                mo_et = market_open.tz_convert('US/Eastern')
                return False, f"Market Opens at {mo_et.strftime('%I:%M %p ET')}"
            else:
                return False, "Market Closed"
                
        except Exception as e:
            logger.exception("Error checking market status")
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
    main()
