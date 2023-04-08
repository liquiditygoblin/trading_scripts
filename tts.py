import pyttsx3
import pygame
from asyncio import run
import ccxt.pro as ccxtpro
import datetime
from decimal import Decimal

engine = pyttsx3.init()
pygame.init()



SMALL_TRADE = 100
BIG_TRADE = 1000
SYMBOL = "ARB/USDT"
TICK_SIZE = Decimal('0.0001') # you could do this in code but each exchange has a diff format so cbf
PAY_THROUGH_TICKS = 0


pygame.mixer.music.load('bonk.wav')

bonk_sound = pygame.mixer.Sound("bonk.wav")


def say(text):
    engine.say(text)
    engine.runAndWait()


def bonk():
    pygame.mixer.Sound.play(bonk_sound)
    pygame.mixer.music.stop()


def num_ticks(price, tick_size):
    return int(Decimal(price) / tick_size)
    

async def main():

    # Instantiate exchange
    exchange = ccxtpro.binance() # you can change this to any exchange ccxt supports
    

    while True:
        trades = await exchange.watch_trades(SYMBOL)
        
        time = datetime.datetime.now() 
        
        buys = []
        sells = []
        
        total_buy = 0
        total_sell = 0
        
        for trade in trades:
            if trade["side"] == "buy":
                buys.append(trade['price'])
                total_buy += trade["amount"]
            else:
                sells.append(trade['price'])
                total_sell += trade["amount"]

        if len(buys) > 1 and abs(num_ticks(buys[0] - buys[-1], TICK_SIZE)) > PAY_THROUGH_TICKS:
            ticks = abs(num_ticks(buys[0] - buys[-1], TICK_SIZE))
            print(f"[{time}] PAY THROUGH {ticks} BUY")
            say(f"aggressive buy {ticks} ticks")
        elif total_buy > BIG_TRADE:
            say("big buy")
            print(f"[{time}] BIG TRADE {total_buy} BUY")
        elif total_buy > SMALL_TRADE:
            bonk()
            print(f"[{time}] TRADE {total_buy} BUY")
            bonk()
        
        if len(sells) > 1 and abs(num_ticks(sells[0] - sells[-1], TICK_SIZE)) > PAY_THROUGH_TICKS:
            ticks = abs(num_ticks(sells[0] - sells[-1], TICK_SIZE))
            print(f"[{time}] PAY THROUGH {ticks} SELL")
            say("aggressive sell, {ticks} ticks")
        elif total_sell > BIG_TRADE:
            say("big sell")
            print(f"[{time}] BIG TRADE {total_sell} SELL")
            
        elif total_sell > SMALL_TRADE:
            print(f"[{time}] TRADE {total_sell} SELL")
            bonk()

        

run(main())
