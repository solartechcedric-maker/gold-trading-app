"""
Gold Trading Indicators - MOBILE OPTIMIZED
No pandas/numpy - pure Python for Android compatibility
"""

class TradingIndicators:
    """Lightweight indicators for mobile"""
    
    def __init__(self):
        self.rsi_period = 14
        self.bb_period = 20
        self.bb_std = 2
        self.stoch_rsi_period = 14
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.atr_period = 14
        self.dmi_period = 14
        self.vortex_period = 14
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI - pure Python"""
        if len(prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        for i in range(len(prices) - period, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    def calculate_stochastic_rsi(self, prices, rsi_period=14, stoch_period=14, k_period=3, d_period=3):
        """Calculate Stochastic RSI"""
        if len(prices) < rsi_period + stoch_period:
            return {'k': 50, 'd': 50, 'signal': 'NEUTRAL', 'in_zone': False}
        
        # Calculate RSI values
        rsi_values = []
        for i in range(rsi_period, len(prices)):
            rsi = self.calculate_rsi(prices[:i+1], rsi_period)
            rsi_values.append(rsi)
        
        if len(rsi_values) < stoch_period:
            return {'k': 50, 'd': 50, 'signal': 'NEUTRAL', 'in_zone': False}
        
        # Stochastic calculation
        recent_rsi = rsi_values[-stoch_period:]
        min_rsi = min(recent_rsi)
        max_rsi = max(recent_rsi)
        
        if max_rsi == min_rsi:
            k_value = 50
        else:
            k_value = 100 * (rsi_values[-1] - min_rsi) / (max_rsi - min_rsi)
        
        d_value = k_value  # Simplified
        
        signal = 'NEUTRAL'
        in_zone = False
        
        if k_value < 20:
            signal = 'OVERSOLD'
            in_zone = True
        elif k_value > 80:
            signal = 'OVERBOUGHT'
            in_zone = True
        
        return {'k': round(k_value, 2), 'd': round(d_value, 2), 'signal': signal, 'in_zone': in_zone}
    
    def calculate_ema(self, prices, period):
        """Calculate EMA"""
        if len(prices) < period:
            return prices[-1]
        
        k = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = price * k + ema * (1 - k)
        
        return round(ema, 2)
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        if len(prices) < slow:
            return {'macd': 0, 'signal': 0, 'histogram': 0, 'trend': 'NEUTRAL'}
        
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line * 0.9  # Simplified
        histogram = macd_line - signal_line
        
        trend = 'BULLISH' if macd_line > signal_line else 'BEARISH'
        
        return {
            'macd': round(macd_line, 2),
            'signal': round(signal_line, 2),
            'histogram': round(histogram, 2),
            'trend': trend
        }
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            current_price = prices[-1]
            return {'upper': current_price * 1.02, 'middle': current_price, 'lower': current_price * 0.98}
        
        recent = prices[-period:]
        mean = sum(recent) / period
        
        # Calculate standard deviation
        variance = sum((x - mean) ** 2 for x in recent) / period
        std = variance ** 0.5
        
        upper = mean + (std * std_dev)
        lower = mean - (std * std_dev)
        
        return {'upper': round(upper, 2), 'middle': round(mean, 2), 'lower': round(lower, 2)}
    
    def calculate_atr(self, highs, lows, closes, period=14):
        """Calculate ATR"""
        if len(closes) < period + 1:
            return {'atr': 5.0, 'volatility': 'NORMAL'}
        
        true_ranges = []
        for i in range(len(closes) - period, len(closes)):
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            true_ranges.append(max(tr1, tr2, tr3))
        
        atr_value = sum(true_ranges) / period
        volatility = 'HIGH' if atr_value > 15 else 'NORMAL' if atr_value > 8 else 'LOW'
        
        return {'atr': round(atr_value, 2), 'volatility': volatility}
    
    def calculate_dmi(self, highs, lows, closes, period=14):
        """Calculate DMI"""
        if len(closes) < period + 1:
            return {'adx': 20, 'plus_di': 20, 'minus_di': 20, 'signal': 'NEUTRAL'}
        
        plus_dm = 0
        minus_dm = 0
        tr = 0
        
        for i in range(len(closes) - period, len(closes)):
            high_diff = highs[i] - highs[i-1]
            low_diff = lows[i-1] - lows[i]
            
            if high_diff > low_diff and high_diff > 0:
                plus_dm += high_diff
            if low_diff > high_diff and low_diff > 0:
                minus_dm += low_diff
            
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            tr += max(tr1, tr2, tr3)
        
        plus_di = 100 * plus_dm / tr if tr > 0 else 20
        minus_di = 100 * minus_dm / tr if tr > 0 else 20
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 20
        adx = dx  # Simplified
        
        signal = 'BULLISH' if plus_di > minus_di else 'BEARISH'
        
        return {'adx': round(adx, 2), 'plus_di': round(plus_di, 2), 'minus_di': round(minus_di, 2), 'signal': signal}
    
    def calculate_vortex(self, highs, lows, closes, period=14):
        """Calculate Vortex"""
        if len(closes) < period + 1:
            return {'vi_plus': 1.0, 'vi_minus': 1.0, 'signal': 'NEUTRAL'}
        
        vm_plus = 0
        vm_minus = 0
        tr = 0
        
        for i in range(len(closes) - period, len(closes)):
            vm_plus += abs(highs[i] - lows[i-1])
            vm_minus += abs(lows[i] - highs[i-1])
            
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            tr += max(tr1, tr2, tr3)
        
        vi_plus = vm_plus / tr if tr > 0 else 1.0
        vi_minus = vm_minus / tr if tr > 0 else 1.0
        
        signal = 'BULLISH' if vi_plus > vi_minus else 'BEARISH'
        
        return {'vi_plus': round(vi_plus, 2), 'vi_minus': round(vi_minus, 2), 'signal': signal}
    
    def calculate_bulb(self, prices, rsi_values):
        """Calculate BULB"""
        if len(prices) < 20:
            return {'signal': 'NEUTRAL', 'momentum': 0, 'rsi': 50}
        
        price_change = ((prices[-1] - prices[-20]) / prices[-20]) * 100
        current_rsi = rsi_values[-1] if rsi_values else 50
        
        momentum = 0
        signal = 'NEUTRAL'
        
        if price_change > 0.5 and current_rsi < 70:
            momentum = min(100, price_change * 10 + (50 - current_rsi))
            signal = 'BULLISH' if momentum > 30 else 'BUY'
        elif price_change < -0.5 and current_rsi > 30:
            momentum = max(-100, price_change * 10 + (50 - current_rsi))
            signal = 'BEARISH' if momentum < -30 else 'SELL'
        
        return {'signal': signal, 'momentum': round(momentum, 2), 'rsi': round(current_rsi, 2)}
    
    def generate_comprehensive_signal(self, current_price, prices, highs=None, lows=None):
        """Generate complete trading signal"""
        if highs is None:
            highs = prices[:]
        if lows is None:
            lows = prices[:]
        
        # Calculate all indicators
        rsi = self.calculate_rsi(prices)
        stoch_rsi = self.calculate_stochastic_rsi(prices)
        macd = self.calculate_macd(prices)
        bb = self.calculate_bollinger_bands(prices)
        atr = self.calculate_atr(highs, lows, prices)
        dmi = self.calculate_dmi(highs, lows, prices)
        vortex = self.calculate_vortex(highs, lows, prices)
        
        # EMA
        ema9 = self.calculate_ema(prices, 9)
        ema21 = self.calculate_ema(prices, 21)
        ema50 = self.calculate_ema(prices, 50)
        ema = {'ema9': ema9, 'ema21': ema21, 'ema50': ema50, 'aligned': ema9 > ema21 > ema50}
        
        # BULB
        rsi_history = [self.calculate_rsi(prices[:i+1]) for i in range(max(14, len(prices)-50), len(prices))]
        bulb = self.calculate_bulb(prices, rsi_history)
        
        # Count signals
        buy_signals = 0
        sell_signals = 0
        
        if rsi < 30:
            buy_signals += 2
        elif rsi > 70:
            sell_signals += 2
        
        if stoch_rsi['signal'] in ['OVERSOLD', 'BUY']:
            buy_signals += 2
        elif stoch_rsi['signal'] in ['OVERBOUGHT', 'SELL']:
            sell_signals += 2
        
        if macd['trend'] == 'BULLISH' and macd['histogram'] > 0:
            buy_signals += 1
        elif macd['trend'] == 'BEARISH' and macd['histogram'] < 0:
            sell_signals += 1
        
        if bulb['signal'] in ['BULLISH', 'BUY']:
            buy_signals += 2
        elif bulb['signal'] in ['BEARISH', 'SELL']:
            sell_signals += 2
        
        if dmi['signal'] == 'BULLISH' and dmi['adx'] > 25:
            buy_signals += 1
        elif dmi['signal'] == 'BEARISH' and dmi['adx'] > 25:
            sell_signals += 1
        
        if vortex['signal'] == 'BULLISH':
            buy_signals += 1
        elif vortex['signal'] == 'BEARISH':
            sell_signals += 1
        
        if current_price <= bb['lower']:
            buy_signals += 1
        elif current_price >= bb['upper']:
            sell_signals += 1
        
        # Generate signal
        total = buy_signals + sell_signals
        if total == 0:
            signal = 'HOLD'
            confidence = 50
        elif buy_signals > sell_signals:
            signal = 'STRONG BUY' if buy_signals >= sell_signals * 2 else 'BUY'
            confidence = min(95, int(50 + (buy_signals / total) * 50))
        elif sell_signals > buy_signals:
            signal = 'STRONG SELL' if sell_signals >= buy_signals * 2 else 'SELL'
            confidence = min(95, int(50 + (sell_signals / total) * 50))
        else:
            signal = 'HOLD'
            confidence = 50
        
        # Reason
        reasons = []
        if rsi < 30:
            reasons.append("RSI oversold")
        elif rsi > 70:
            reasons.append("RSI overbought")
        if stoch_rsi['in_zone']:
            reasons.append(f"Stoch {stoch_rsi['signal'].lower()}")
        if bulb['signal'] in ['BULLISH', 'BEARISH', 'BUY', 'SELL']:
            reasons.append(f"BULB {bulb['signal'].lower()}")
        if current_price <= bb['lower']:
            reasons.append("At lower BB")
        elif current_price >= bb['upper']:
            reasons.append("At upper BB")
        
        reason = " + ".join(reasons) if reasons else "Wait for setup"
        
        return {
            'signal': signal,
            'confidence': confidence,
            'reason': reason,
            'indicators': {
                'rsi': rsi,
                'stoch_rsi': stoch_rsi,
                'macd': macd,
                'ema': ema,
                'bollinger_bands': bb,
                'atr': atr,
                'dmi': dmi,
                'vortex': vortex,
                'bulb': bulb
            },
            'buy_count': buy_signals,
            'sell_count': sell_signals
        }
    
    def get_rsi_status(self, rsi):
        """Get RSI status"""
        if rsi < 30:
            return "OVERSOLD", "green"
        elif rsi > 70:
            return "OVERBOUGHT", "red"
        elif rsi < 40:
            return "Weak", "orange"
        elif rsi > 60:
            return "Strong", "orange"
        else:
            return "Neutral", "gray"
    
    def get_bb_position(self, current_price, bb):
        """Get BB position"""
        if current_price >= bb['upper']:
            return "At Upper Band", "red"
        elif current_price <= bb['lower']:
            return "At Lower Band", "green"
        elif current_price > bb['middle']:
            return "Above Middle", "orange"
        elif current_price < bb['middle']:
            return "Below Middle", "orange"
        else:
            return "At Middle", "gray"
