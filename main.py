import yfinance as yf
from time import time, sleep
import os
import asciiart
from datetime import datetime

# readin Stock and refresh rate
with open("settings.txt") as f:
    first_line = f.readline()
    second_line = f.readline()

STOCK = first_line[6:].strip()
RATE= int(second_line[12:].strip())

#data from yfinance stock + color and ascii arrows
def data(stock):
    msft = yf.Ticker(stock)

    data_month = msft.history(period="1mo")
    data_month_ago = data_month.iloc[0, 3]
    data_yesterday = data_month.iloc[-2, 3]
    data_live = data_month.iloc[-1, 3]

    data_live_ticker = msft.info.get("regularMarketPrice")
    data_symbol = msft.info.get("symbol")
    data_live_zeit = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    data_change_yesterday = ((data_live - data_yesterday) / data_yesterday) * 100
    data_change_month = ((data_live - data_month_ago) / data_month_ago) * 100

    print(data_symbol)
    print(data_live_zeit)
    print("-------------------")
    print("Live:       ", round(data_live, 2))
    print(
        "Yesterday: ",
        clour_check(data_change_yesterday),
        round(data_change_yesterday, 2),
        "%",
        "\033[1;37;40m    ",
        "Monthago:",
        clour_check(data_change_month),
        round(data_change_month, 2),
        "%",)
    print("")
    for i in range(5):
        print(
            "     ",
            clour_check(data_change_yesterday),
            arrow(data_change_yesterday)[i],
            "        ",
            clour_check(data_change_month),
            arrow(data_change_month)[i],
        )
    print("\033[1;37;40m ")

# color check
def clour_check(data_change):
    if data_change > 0:
        return "\033[1;32;40m"
    elif data_change == 0:
        return "\033[1;30;40m"
    elif data_change < 0:
        return "\033[1;31;40m"

# arrow 
def arrow(data_change):
    if data_change > 0:
        return asciiart.arrowup
    elif data_change == 0:
        return asciiart.arrowside
    elif data_change < 0:
        return asciiart.arrowdown


data(STOCK)
os.system("cls" if os.name == "nt" else "clear")
while True:
    data(STOCK)
    sleep(RATE)
    os.system("cls" if os.name == "nt" else "clear")
