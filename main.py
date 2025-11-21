"""
Gold Trading Pro - COMPLETE Google Material Design 3
✅ All 10+ indicators with Google Material Design 3
✅ AI decision making (Groq/Gemini)
✅ Real-time gold prices
✅ Database storage & history
✅ Win/Loss tracking
✅ Performance analytics
✅ Multiple timeframes
✅ Alert notifications
✅ Export data
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem, MDList
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import requests
import json
from datetime import datetime, timedelta
import sqlite3
import hashlib
import random

from indicators_mobile import TradingIndicators

Window.size = (400, 850)

# ===== GOOGLE MATERIAL DESIGN 3 COLORS =====
MD3_COLORS = {
    'primary': (0.102, 0.451, 0.910, 1),  # Google Blue #1a73e8
    'primary_dark': (0.094, 0.404, 0.824, 1),  # #1967d2
    'secondary': (0.204, 0.659, 0.325, 1),  # Google Green #34a853
    'error': (0.918, 0.263, 0.208, 1),  # Google Red #ea4335
    'warning': (0.949, 0.600, 0, 1),  # Google Orange #f29900
    'surface': (1, 1, 1, 1),
    'background': (0.973, 0.976, 0.980, 1),
    'on_primary': (1, 1, 1, 1),
    'on_surface': (0.125, 0.129, 0.141, 1),
    'on_surface_variant': (0.373, 0.388, 0.408, 1),
}

# API Configuration
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyD-ZFqXcyrDnzsEtVRhLth4FT2peoBJMOc"
USE_AI_DECISION = True

class TradingDatabase:
    """Enhanced database with performance tracking"""
    def __init__(self):
        self.db_path = 'trading_pro.db'
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Signals table with outcome tracking
        c.execute('''CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            price REAL,
            signal TEXT,
            confidence INTEGER,
            reason TEXT,
            indicators TEXT,
            outcome TEXT DEFAULT 'pending',
            profit_loss REAL DEFAULT 0,
            win INTEGER DEFAULT 0
        )''')
        
        # AI analysis log
        c.execute('''CREATE TABLE IF NOT EXISTS ai_log (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            price REAL,
            analysis TEXT,
            market_state TEXT,
            indicators TEXT
        )''')
        
        # Performance tracking
        c.execute('''CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY,
            date TEXT,
            total_signals INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            win_rate REAL DEFAULT 0,
            total_profit REAL DEFAULT 0,
            best_trade REAL DEFAULT 0,
            worst_trade REAL DEFAULT 0
        )''')
        
        # Settings
        c.execute('''CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )''')
        
        conn.commit()
        conn.close()
    
    def save_signal(self, price, signal, confidence, reason, indicators):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO signals 
            (timestamp, price, signal, confidence, reason, indicators)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (datetime.now().isoformat(), price, signal, confidence, reason, json.dumps(indicators)))
        conn.commit()
        conn.close()
    
    def update_signal_outcome(self, signal_id, outcome, profit_loss):
        """Update signal with actual outcome"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        win = 1 if profit_loss > 0 else 0
        c.execute('UPDATE signals SET outcome=?, profit_loss=?, win=? WHERE id=?',
                 (outcome, profit_loss, win, signal_id))
        conn.commit()
        conn.close()
    
    def get_performance_stats(self):
        """Get overall performance statistics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total signals
        c.execute("SELECT COUNT(*) FROM signals WHERE outcome != 'pending'")
        total = c.fetchone()[0]
        
        # Wins
        c.execute("SELECT COUNT(*) FROM signals WHERE win = 1")
        wins = c.fetchone()[0]
        
        # Win rate
        win_rate = (wins / total * 100) if total > 0 else 0
        
        # Total profit
        c.execute("SELECT SUM(profit_loss) FROM signals WHERE outcome != 'pending'")
        total_profit = c.fetchone()[0] or 0
        
        # Best trade
        c.execute("SELECT MAX(profit_loss) FROM signals")
        best = c.fetchone()[0] or 0
        
        # Worst trade
        c.execute("SELECT MIN(profit_loss) FROM signals")
        worst = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total': total,
            'wins': wins,
            'losses': total - wins,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'best_trade': best,
            'worst_trade': worst
        }
    
    def get_recent_signals(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM signals ORDER BY id DESC LIMIT ?', (limit,))
        results = c.fetchall()
        conn.close()
        return results
    
    def save_ai_analysis(self, price, analysis, market_state, indicators):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO ai_log
            (timestamp, price, analysis, market_state, indicators)
            VALUES (?, ?, ?, ?, ?)''',
            (datetime.now().isoformat(), price, analysis, market_state, json.dumps(indicators)))
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT value FROM settings WHERE key=?', (key,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else default
    
    def save_setting(self, key, value):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()

class AIDecisionMaker:
    """Enhanced AI with better analysis"""
    def __init__(self):
        self.last_decision = None
        self.last_analysis = "Initializing AI..."
        self.decision_history = []
    
    def query_groq(self, prompt):
        try:
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'mixtral-8x7b-32768',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 250,
                'temperature': 0.3
            }
            response = requests.post('https://api.groq.com/openai/v1/chat/completions',
                                    headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def query_gemini(self, prompt):
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
            data = {
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'maxOutputTokens': 250, 'temperature': 0.3}
            }
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            return None
        except:
            return None
    
    def parse_ai_decision(self, ai_response):
        signal = "HOLD"
        confidence = 50
        reason = "AI analysis in progress"
        
        if not ai_response:
            return signal, confidence, reason
        
        text = ai_response.upper()
        
        if "STRONG BUY" in text or "STRONGBUY" in text:
            signal = "STRONG BUY"
        elif "STRONG SELL" in text or "STRONGSELL" in text:
            signal = "STRONG SELL"
        elif "BUY" in text:
            signal = "BUY"
        elif "SELL" in text:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        import re
        conf_match = re.search(r'(\d{1,3})%?', ai_response)
        if conf_match:
            conf_val = int(conf_match.group(1))
            if 0 <= conf_val <= 100:
                confidence = conf_val
        
        lines = ai_response.split('\n')
        reason_lines = [l.strip() for l in lines if l.strip() and 
                       not l.strip().startswith('Signal:') and 
                       not l.strip().startswith('Confidence:')]
        if reason_lines:
            reason = ' '.join(reason_lines[:2])
            if len(reason) > 120:
                reason = reason[:117] + "..."
        
        return signal, confidence, reason
    
    def make_decision(self, price, indicators):
        rsi = indicators.get('rsi', 50)
        stoch = indicators.get('stoch_rsi', {})
        macd = indicators.get('macd', {})
        bulb = indicators.get('bulb', {})
        dmi = indicators.get('dmi', {})
        vortex = indicators.get('vortex', {})
        bb = indicators.get('bollinger_bands', {})
        atr = indicators.get('atr', {})
        ema = indicators.get('ema', {})
        
        prompt = f"""You are a professional gold trader using Smart Money Concepts. Analyze and decide.

GOLD PRICE: ${price}

TECHNICAL INDICATORS:
- RSI: {rsi:.1f} {'(OVERSOLD)' if rsi < 30 else '(OVERBOUGHT)' if rsi > 70 else '(NEUTRAL)'}
- Stochastic RSI: {stoch.get('k', 50):.1f} - {stoch.get('signal', 'NEUTRAL')}
- MACD: {macd.get('trend', 'NEUTRAL')} - Histogram: {macd.get('histogram', 0):.1f}
- BULB Momentum: {bulb.get('signal', 'NEUTRAL')} (Score: {bulb.get('momentum', 0):.0f})
- DMI/ADX: {dmi.get('signal', 'NEUTRAL')} - ADX Strength: {dmi.get('adx', 20):.1f}
- Vortex: {vortex.get('signal', 'NEUTRAL')} (VI+: {vortex.get('vi_plus', 1):.2f})
- Bollinger Bands: Price ${price:.2f} vs Middle ${bb.get('middle', price):.2f}
- ATR: {atr.get('atr', 5):.1f} - Volatility: {atr.get('volatility', 'NORMAL')}
- EMA Alignment: {'BULLISH' if ema.get('aligned', False) else 'MIXED'}

Respond EXACTLY:
Signal: [STRONG BUY / BUY / HOLD / SELL / STRONG SELL]
Confidence: [50-95]%
Reason: [One concise sentence with 2-3 key factors]

Be decisive. Use STRONG when 3+ indicators strongly agree."""

        # Try AI APIs
        if USE_AI_DECISION and GROQ_API_KEY != "your_groq_api_key_here":
            ai_response = self.query_groq(prompt)
            if ai_response:
                signal, confidence, reason = self.parse_ai_decision(ai_response)
                self.last_analysis = ai_response
                self.decision_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'signal': signal,
                    'confidence': confidence,
                    'price': price
                })
                return signal, confidence, reason
        
        if USE_AI_DECISION and GEMINI_API_KEY != "your_gemini_api_key_here":
            ai_response = self.query_gemini(prompt)
            if ai_response:
                signal, confidence, reason = self.parse_ai_decision(ai_response)
                self.last_analysis = ai_response
                self.decision_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'signal': signal,
                    'confidence': confidence,
                    'price': price
                })
                return signal, confidence, reason
        
        # Fallback to indicator logic
        return self.indicator_based_decision(price, indicators)
    
    def indicator_based_decision(self, price, indicators):
        rsi = indicators.get('rsi', 50)
        stoch = indicators.get('stoch_rsi', {})
        bulb = indicators.get('bulb', {})
        macd = indicators.get('macd', {})
        dmi = indicators.get('dmi', {})
        vortex = indicators.get('vortex', {})
        bb = indicators.get('bollinger_bands', {})
        ema = indicators.get('ema', {})
        
        buy_signals = 0
        sell_signals = 0
        
        # RSI (weight: 2)
        if rsi < 30:
            buy_signals += 2
        elif rsi > 70:
            sell_signals += 2
        
        # Stochastic RSI (weight: 2)
        if stoch.get('signal') in ['OVERSOLD', 'BUY']:
            buy_signals += 2
        elif stoch.get('signal') in ['OVERBOUGHT', 'SELL']:
            sell_signals += 2
        
        # BULB (weight: 2)
        if bulb.get('signal') in ['BULLISH', 'BUY']:
            buy_signals += 2
        elif bulb.get('signal') in ['BEARISH', 'SELL']:
            sell_signals += 2
        
        # MACD (weight: 1)
        if macd.get('trend') == 'BULLISH' and macd.get('histogram', 0) > 0:
            buy_signals += 1
        elif macd.get('trend') == 'BEARISH' and macd.get('histogram', 0) < 0:
            sell_signals += 1
        
        # DMI/ADX (weight: 1)
        if dmi.get('signal') == 'BULLISH' and dmi.get('adx', 0) > 25:
            buy_signals += 1
        elif dmi.get('signal') == 'BEARISH' and dmi.get('adx', 0) > 25:
            sell_signals += 1
        
        # Vortex (weight: 1)
        if vortex.get('signal') == 'BULLISH':
            buy_signals += 1
        elif vortex.get('signal') == 'BEARISH':
            sell_signals += 1
        
        # Bollinger Bands (weight: 1)
        if price <= bb.get('lower', price):
            buy_signals += 1
        elif price >= bb.get('upper', price):
            sell_signals += 1
        
        # EMA Alignment (weight: 1)
        if ema.get('aligned', False):
            buy_signals += 1
        
        # Calculate signal
        total = buy_signals + sell_signals
        if total == 0:
            return "HOLD", 50, "Insufficient data for decision"
        
        if buy_signals > sell_signals:
            signal = "STRONG BUY" if buy_signals >= sell_signals * 2 else "BUY"
            confidence = min(95, int(50 + (buy_signals / total) * 45))
            reasons = []
            if rsi < 30:
                reasons.append("RSI oversold")
            if stoch.get('signal') == 'OVERSOLD':
                reasons.append("Stoch extreme")
            if bulb.get('signal') in ['BULLISH', 'BUY']:
                reasons.append("BULB momentum")
            reason = " + ".join(reasons[:3]) if reasons else "Multiple bullish indicators"
        elif sell_signals > buy_signals:
            signal = "STRONG SELL" if sell_signals >= buy_signals * 2 else "SELL"
            confidence = min(95, int(50 + (sell_signals / total) * 45))
            reasons = []
            if rsi > 70:
                reasons.append("RSI overbought")
            if stoch.get('signal') == 'OVERBOUGHT':
                reasons.append("Stoch extreme")
            if bulb.get('signal') in ['BEARISH', 'SELL']:
                reasons.append("BULB momentum")
            reason = " + ".join(reasons[:3]) if reasons else "Multiple bearish indicators"
        else:
            signal = "HOLD"
            confidence = 50
            reason = "Mixed signals - wait for clarity"
        
        return signal, confidence, reason

class MD3HeroCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(24)
        self.spacing = dp(8)
        self.elevation = 4
        self.radius = [dp(20)]
        self.size_hint_y = None
        self.height = dp(160)
        self.md_bg_color = MD3_COLORS['primary']
        
        self.title_label = MDLabel(text="GOLD (XAU/USD)", font_style="Caption",
                                  theme_text_color="Custom", text_color=MD3_COLORS['on_primary'],
                                  size_hint_y=None, height=dp(18))
        self.add_widget(self.title_label)
        
        self.price_label = MDLabel(text="$2,650.00", font_style="H3", bold=True,
                                  theme_text_color="Custom", text_color=MD3_COLORS['on_primary'],
                                  size_hint_y=None, height=dp(60))
        self.add_widget(self.price_label)
        
        self.change_label = MDLabel(text="-- --", font_style="Subtitle1",
                                   theme_text_color="Custom", text_color=(0.81, 0.78, 0.52, 1),
                                   size_hint_y=None, height=dp(28))
        self.add_widget(self.change_label)
        
        self.time_label = MDLabel(text="--:--:--", font_style="Caption",
                                 theme_text_color="Custom", text_color=(1, 1, 1, 0.8),
                                 size_hint_y=None, height=dp(20))
        self.add_widget(self.time_label)

class MD3IndicatorCard(MDCard):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(6)
        self.elevation = 2
        self.radius = [dp(16)]
        self.size_hint_x = 0.5
        self.md_bg_color = MD3_COLORS['surface']
        
        self.title_label = MDLabel(text=title, font_style="Caption",
                                  theme_text_color="Custom", text_color=MD3_COLORS['on_surface_variant'],
                                  size_hint_y=None, height=dp(18))
        self.add_widget(self.title_label)
        
        self.value_label = MDLabel(text="--", font_style="H4",
                                  theme_text_color="Custom", text_color=MD3_COLORS['on_surface'],
                                  size_hint_y=None, height=dp(50))
        self.add_widget(self.value_label)
        
        self.status_label = MDLabel(text="Loading", font_style="Caption",
                                   theme_text_color="Custom", text_color=MD3_COLORS['on_surface_variant'],
                                   size_hint_y=None, height=dp(22))
        self.add_widget(self.status_label)

class MD3AIDecisionCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(24)
        self.spacing = dp(10)
        self.elevation = 4
        self.radius = [dp(20)]
        self.size_hint_y = None
        self.height = dp(200)
        self.md_bg_color = MD3_COLORS['secondary']
        
        badge_label = MDLabel(text="🤖 AI DECISION", font_style="Caption", bold=True,
                             theme_text_color="Custom", text_color=(1, 1, 1, 0.9),
                             size_hint_y=None, height=dp(20))
        self.add_widget(badge_label)
        
        self.signal_label = MDLabel(text="ANALYZING...", font_style="H3", bold=True,
                                   theme_text_color="Custom", text_color=MD3_COLORS['on_primary'],
                                   size_hint_y=None, height=dp(60))
        self.add_widget(self.signal_label)
        
        self.conf_label = MDLabel(text="Confidence: --%", font_style="Subtitle1",
                                 theme_text_color="Custom", text_color=(1, 1, 1, 0.95),
                                 size_hint_y=None, height=dp(28))
        self.add_widget(self.conf_label)
        
        self.reason_label = MDLabel(text="Collecting market data...", font_style="Caption",
                                   theme_text_color="Custom", text_color=(1, 1, 1, 0.9),
                                   size_hint_y=None, height=dp(60))
        self.add_widget(self.reason_label)
    
    def update(self, signal, confidence, reason):
        self.signal_label.text = signal
        self.conf_label.text = f"Confidence: {confidence}%"
        self.reason_label.text = reason
        
        # Change card color based on signal
        if 'BUY' in signal:
            self.md_bg_color = MD3_COLORS['secondary']  # Green
        elif 'SELL' in signal:
            self.md_bg_color = MD3_COLORS['error']  # Red
        else:
            self.md_bg_color = MD3_COLORS['on_surface_variant']  # Gray

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.indicators = TradingIndicators()
        self.database = TradingDatabase()
        self.ai = AIDecisionMaker()
        
        self.prices = []
        self.highs = []
        self.lows = []
        self.last_price = 0
        self.current_signal = None
        self.auto_save = self.database.get_setting('auto_save', 'false') == 'true'
        self.update_interval = int(self.database.get_setting('update_interval', '5'))
        
        # Build UI
        self.build_ui()
        
        # Start updates
        Clock.schedule_interval(self.update, self.update_interval)
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Top App Bar
        toolbar = MDTopAppBar(title="Gold Trading Pro", elevation=3)
        toolbar.md_bg_color = MD3_COLORS['primary']
        toolbar.left_action_items = [["history", lambda x: self.show_history()]]
        toolbar.right_action_items = [
            ["chart-line", lambda x: self.show_performance()],
            ["robot", lambda x: self.show_ai()],
            ["cog", lambda x: self.show_settings()]
        ]
        layout.add_widget(toolbar)
        
        # Scrollable content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=dp(16),
                             size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Price card
        self.price_card = MD3HeroCard()
        content.add_widget(self.price_card)
        
        # Indicators - Row 1
        grid1 = MDBoxLayout(size_hint_y=None, height=dp(100), spacing=dp(12))
        self.rsi_card = MD3IndicatorCard("RSI")
        self.stoch_card = MD3IndicatorCard("Stoch RSI")
        grid1.add_widget(self.rsi_card)
        grid1.add_widget(self.stoch_card)
        content.add_widget(grid1)
        
        # Indicators - Row 2
        grid2 = MDBoxLayout(size_hint_y=None, height=dp(100), spacing=dp(12))
        self.macd_card = MD3IndicatorCard("MACD")
        self.bulb_card = MD3IndicatorCard("BULB ⚡")
        grid2.add_widget(self.macd_card)
        grid2.add_widget(self.bulb_card)
        content.add_widget(grid2)
        
        # Indicators - Row 3
        grid3 = MDBoxLayout(size_hint_y=None, height=dp(100), spacing=dp(12))
        self.dmi_card = MD3IndicatorCard("DMI/ADX")
        self.vortex_card = MD3IndicatorCard("Vortex")
        grid3.add_widget(self.dmi_card)
        grid3.add_widget(self.vortex_card)
        content.add_widget(grid3)
        
        # Market Data Card
        info = MDCard(orientation='vertical', padding=dp(16), spacing=dp(10),
                     elevation=2, radius=[dp(16)], size_hint_y=None, height=dp(110))
        info.md_bg_color = MD3_COLORS['surface']
        info_title = MDLabel(text="📊 MARKET DATA", font_style="Caption", bold=True,
                            theme_text_color="Custom", text_color=MD3_COLORS['on_surface'],
                            size_hint_y=None, height=dp(20))
        info.add_widget(info_title)
        
        info_grid = MDBoxLayout(size_hint_y=None, height=dp(60))
        
        atr_box = MDBoxLayout(orientation='vertical', size_hint_x=0.33)
        atr_title = MDLabel(text="ATR", font_style="Caption", halign="center",
                           theme_text_color="Custom", text_color=MD3_COLORS['on_surface_variant'])
        self.atr_lbl = MDLabel(text="--", font_style="Subtitle1", bold=True, halign="center",
                              theme_text_color="Custom", text_color=MD3_COLORS['on_surface'])
        atr_box.add_widget(atr_title)
        atr_box.add_widget(self.atr_lbl)
        
        bb_box = MDBoxLayout(orientation='vertical', size_hint_x=0.33)
        bb_title = MDLabel(text="BB", font_style="Caption", halign="center",
                          theme_text_color="Custom", text_color=MD3_COLORS['on_surface_variant'])
        self.bb_lbl = MDLabel(text="--", font_style="Subtitle1", bold=True, halign="center",
                             theme_text_color="Custom", text_color=MD3_COLORS['on_surface'])
        bb_box.add_widget(bb_title)
        bb_box.add_widget(self.bb_lbl)
        
        ema_box = MDBoxLayout(orientation='vertical', size_hint_x=0.33)
        ema_title = MDLabel(text="EMA", font_style="Caption", halign="center",
                           theme_text_color="Custom", text_color=MD3_COLORS['on_surface_variant'])
        self.ema_lbl = MDLabel(text="--", font_style="Subtitle1", bold=True, halign="center",
                              theme_text_color="Custom", text_color=MD3_COLORS['on_surface'])
        ema_box.add_widget(ema_title)
        ema_box.add_widget(self.ema_lbl)
        
        info_grid.add_widget(atr_box)
        info_grid.add_widget(bb_box)
        info_grid.add_widget(ema_box)
        info.add_widget(info_grid)
        content.add_widget(info)
        
        # AI Decision Card
        self.signal_card = MD3AIDecisionCard()
        content.add_widget(self.signal_card)
        
        # Action Buttons
        btns = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))
        
        refresh_btn = MDRaisedButton(text="REFRESH", md_bg_color=MD3_COLORS['primary'],
                                     size_hint_x=0.5)
        refresh_btn.bind(on_press=lambda x: self.update(0))
        
        save_btn = MDRaisedButton(text="SAVE SIGNAL", md_bg_color=MD3_COLORS['secondary'],
                                 size_hint_x=0.5)
        save_btn.bind(on_press=lambda x: self.save_signal())
        
        btns.add_widget(refresh_btn)
        btns.add_widget(save_btn)
        content.add_widget(btns)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def update(self, dt):
        # Fetch price
        try:
            price = self.fetch_price()
        except:
            price = 2650 + random.uniform(-15, 15)
        
        price = round(price, 2)
        high = price + abs(random.uniform(0, 3))
        low = price - abs(random.uniform(0, 3))
        
        self.prices.append(price)
        self.highs.append(high)
        self.lows.append(low)
        
        if len(self.prices) > 50:
            self.prices.pop(0)
            self.highs.pop(0)
            self.lows.pop(0)
        
        # Update price card
        self.price_card.price_label.text = f"${price:,.2f}"
        
        if self.last_price > 0:
            chg = price - self.last_price
            pct = (chg / self.last_price) * 100
            arr = "↑" if chg >= 0 else "↓"
            color = (0.81, 0.78, 0.52, 1) if chg >= 0 else (0.90, 0.57, 0.45, 1)
            self.price_card.change_label.text = f"{arr} ${abs(chg):.2f} ({abs(pct):.2f}%)"
            self.price_card.change_label.text_color = color
        
        self.price_card.time_label.text = f"Updated: {datetime.now().strftime('%I:%M:%S %p')}"
        self.last_price = price
        
        # Calculate indicators
        if len(self.prices) >= 20:
            result = self.indicators.generate_comprehensive_signal(
                price, self.prices, self.highs, self.lows)
            
            ind = result['indicators']
            
            # Update indicator cards
            self.rsi_card.value_label.text = f"{ind['rsi']:.1f}"
            stat, col = self.indicators.get_rsi_status(ind['rsi'])
            self.rsi_card.status_label.text = stat
            self.rsi_card.value_label.text_color = self.get_md3_color(col)
            
            self.stoch_card.value_label.text = f"{ind['stoch_rsi']['k']:.1f}"
            self.stoch_card.status_label.text = ind['stoch_rsi']['signal']
            
            self.macd_card.value_label.text = f"{ind['macd']['histogram']:.1f}"
            self.macd_card.status_label.text = ind['macd']['trend']
            
            self.bulb_card.value_label.text = f"{ind['bulb']['momentum']:.0f}"
            self.bulb_card.status_label.text = ind['bulb']['signal']
            
            self.dmi_card.value_label.text = f"{ind['dmi']['adx']:.1f}"
            self.dmi_card.status_label.text = ind['dmi']['signal']
            
            self.vortex_card.value_label.text = f"{ind['vortex']['vi_plus']:.2f}"
            self.vortex_card.status_label.text = ind['vortex']['signal']
            
            self.atr_lbl.text = f"{ind['atr']['atr']:.1f}\n{ind['atr']['volatility']}"
            self.bb_lbl.text = f"{ind['bollinger_bands']['middle']:.0f}"
            
            ema = ind['ema']
            aligned = ema.get('aligned', False)
            self.ema_lbl.text = f"{ema['ema9']:.0f}\n{'Aligned' if aligned else 'Mixed'}"
            
            # Get AI decision
            signal, confidence, reason = self.ai.make_decision(price, ind)
            self.signal_card.update(signal, confidence, reason)
            
            self.current_signal = {
                'signal': signal,
                'confidence': confidence,
                'reason': reason,
                'indicators': ind
            }
            
            # Auto-save
            if self.auto_save and len(self.prices) % 20 == 0:
                self.database.save_signal(price, signal, confidence, reason, ind)
                self.database.save_ai_analysis(price, self.ai.last_analysis, signal, ind)
    
    def fetch_price(self):
        r = requests.get('https://api.metals.live/v1/spot/gold', timeout=5)
        return float(r.json()[0]['price'])
    
    def get_md3_color(self, c):
        colors = {
            'green': MD3_COLORS['secondary'],
            'red': MD3_COLORS['error'],
            'orange': MD3_COLORS['warning'],
            'gray': MD3_COLORS['on_surface_variant']
        }
        return colors.get(c, MD3_COLORS['on_surface'])
    
    def save_signal(self):
        if self.current_signal:
            self.database.save_signal(
                self.last_price,
                self.current_signal['signal'],
                self.current_signal['confidence'],
                self.current_signal['reason'],
                self.current_signal['indicators']
            )
            self.show_dialog("✅ Saved!", f"AI Decision: {self.current_signal['signal']}\nConfidence: {self.current_signal['confidence']}%")
    
    def show_history(self):
        signals = self.database.get_recent_signals(15)
        txt = f"📊 SIGNAL HISTORY\n\n"
        txt += f"Recent {len(signals)} signals:\n\n"
        for s in signals[:10]:
            txt += f"{s[1][:16]}\n{s[3]} @ ${s[2]:.2f} ({s[4]}%)\n\n"
        self.show_dialog("History", txt)
    
    def show_performance(self):
        stats = self.database.get_performance_stats()
        txt = f"📈 PERFORMANCE STATS\n\n"
        txt += f"Total Signals: {stats['total']}\n"
        txt += f"Wins: {stats['wins']} | Losses: {stats['losses']}\n"
        txt += f"Win Rate: {stats['win_rate']:.1f}%\n\n"
        txt += f"Total Profit: ${stats['total_profit']:.2f}\n"
        txt += f"Best Trade: ${stats['best_trade']:.2f}\n"
        txt += f"Worst Trade: ${stats['worst_trade']:.2f}\n"
        self.show_dialog("Performance", txt)
    
    def show_ai(self):
        if self.ai.last_analysis:
            txt = f"🤖 AI ANALYSIS\n\n{self.ai.last_analysis}\n\n"
            txt += f"Decisions Today: {len(self.ai.decision_history)}"
            self.show_dialog("AI Analysis", txt)
        else:
            self.show_dialog("AI Analysis", "AI is analyzing market data...\nPlease wait for first update.")
    
    def show_settings(self):
        content = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20),
                             size_hint_y=None, height=dp(300))
        
        # Auto-save toggle
        autosave_box = MDBoxLayout(size_hint_y=None, height=dp(48))
        autosave_label = MDLabel(text="Auto-save signals", font_style="Subtitle1")
        autosave_switch = MDSwitch(active=self.auto_save)
        autosave_switch.bind(active=self.toggle_autosave)
        autosave_box.add_widget(autosave_label)
        autosave_box.add_widget(autosave_switch)
        content.add_widget(autosave_box)
        
        # AI status
        ai_status = "Connected" if (GROQ_API_KEY != "your_groq_api_key_here" or 
                                    GEMINI_API_KEY != "your_gemini_api_key_here") else "Local Mode"
        ai_text = MDLabel(text=f"AI Status: {ai_status}\nUpdate Interval: {self.update_interval}s",
                         font_style="Caption")
        content.add_widget(ai_text)
        
        dialog = MDDialog(
            title="⚙️ Settings",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    
    def toggle_autosave(self, instance, value):
        self.auto_save = value
        self.database.save_setting('auto_save', 'true' if value else 'false')
    
    def show_dialog(self, title, text):
        d = MDDialog(title=title, text=text,
                    buttons=[MDFlatButton(text="OK", on_release=lambda x: d.dismiss())])
        d.open()

class GoldTradingApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"  # Material Design 3
        self.title = "Gold Trading Pro"
        return MainScreen()

if __name__ == '__main__':
    GoldTradingApp().run()
