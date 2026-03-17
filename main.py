import requests
import schedule
import time
from scraper import get_traders
from scorer import filter_traders, score_traders
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SEND_TIME

def send_telegram(message):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def run_bot():
    print("Fetching traders...")
    traders = get_traders()
    print("Found " + str(len(traders)) + " traders")
    filtered = filter_traders(traders)
    print(str(len(filtered)) + " passed filters")
    top = score_traders(filtered)
    if not top:
        send_telegram("No qualifying wallets found today.")
        return
    message = "Top Polymarket Wallets Today\n\n"
    for i, t in enumerate(top, 1):
        message += "#" + str(i) + " Score: " + str(t["score"]) + "/100\n"
        message += "Wallet: " + t["address"] + "\n"
        message += "Win Rate: " + str(t["win_rate"]) + "%\n"
        message += "Trades/Day: " + str(t["trades_per_day"]) + "\n"
        message += "Copiers: " + str(t["copiers"]) + "\n"
        message += "30d Profit: $" + str(round(t["profit_30d"], 2)) + "\n"
        message += "https://polymarket.com/profile/" + t["address"] + "\n\n"
    send_telegram(message)
    print("Message sent!")

schedule.every().day.at(SEND_TIME).do(run_bot)
print("Bot running")
run_bot()
while True:
    schedule.run_pending()
    time.sleep(60)
