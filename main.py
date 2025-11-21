from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

class GoldApp(App):
    def build(self):
        self.price = 2650.00
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Gold Trading Pro', size_hint=(1, 0.2), font_size='24sp', bold=True)
        layout.add_widget(title)
        
        self.price_label = Label(text=f'${self.price:.2f}', size_hint=(1, 0.4), font_size='48sp', bold=True)
        layout.add_widget(self.price_label)
        
        self.signal_label = Label(text='Signal: HOLD', size_hint=(1, 0.2), font_size='20sp')
        layout.add_widget(self.signal_label)
        
        refresh_btn = Button(text='REFRESH PRICE', size_hint=(1, 0.2), font_size='18sp')
        refresh_btn.bind(on_press=self.update_price)
        layout.add_widget(refresh_btn)
        
        Clock.schedule_interval(self.update_price, 5)
        return layout
    
    def update_price(self, *args):
        self.price = round(2650 + random.uniform(-50, 50), 2)
        self.price_label.text = f'${self.price:.2f}'
        
        if self.price > 2700:
            self.signal_label.text = 'Signal: SELL (Overbought)'
        elif self.price < 2600:
            self.signal_label.text = 'Signal: BUY (Oversold)'
        else:
            self.signal_label.text = 'Signal: HOLD (Neutral)'

if __name__ == '__main__':
    GoldApp().run()
