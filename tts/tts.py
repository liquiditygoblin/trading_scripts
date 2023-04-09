import pyttsx3
import pygame
from asyncio import run
import ccxt.base.errors
import ccxt.pro as ccxtpro
import datetime
from decimal import Decimal
import json

with open('config.json', 'r') as f:
    config = json.load(f)

SMALL_TRADE = config['SMALL_TRADE']
BIG_TRADE = config['BIG_TRADE']
SYMBOL = config['SYMBOL']
TICK_SIZE = Decimal(float(config['TICK_SIZE']))  # you could do this in code but each exchange has a diff format so cbf
PAY_THROUGH_TICKS = int(config['PAY_THROUGH_TICKS'])
SOUND_FILE = config['SOUND_FILE']
EXCHANGE = config['EXCHANGE']

engine = pyttsx3.init()
pygame.init()
pygame.mixer.music.load(SOUND_FILE)
bonk_sound = pygame.mixer.Sound(SOUND_FILE)

print("Based on an silly idea by @liquiditygoblin")

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
    try:
        class_ = getattr(ccxtpro, EXCHANGE)
    except AttributeError:
        print("Invalid exchange name")
        exit(0)
    else:
        exchange = class_()
    # Check if the symbol exist
    try:
        await exchange.watch_trades(SYMBOL)
    except ccxt.BadSymbol:
        print("Bad symbol {} doesn't exist on {} bozo".format(SYMBOL, exchange))
        await exchange.close()
        exit(84)
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


if __name__ == '__main__':
    run(main())
