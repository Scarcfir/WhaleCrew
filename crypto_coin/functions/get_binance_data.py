from binance.client import Client
import pytz, dateparser
from datetime import datetime


def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


client = Client("", "")
symbol = "ETHUSDT"
year = datetime.now().year
interval = Client.KLINE_INTERVAL_1DAY
m = datetime.now().month
day = datetime.now().day

month = {'1': 'Jan',
         '2': 'Feb',
         '3': 'Mar',
         '4': 'Apr',
         '5': 'May',
         '6': 'Jun',
         '7': 'Jul',
         '8': 'Aug',
         '9': 'Sep',
         '10': 'Oct',
         '11': 'Nov',
         '12': 'Dec'}

data = f"{day} {month[f'{m}']}, {year}"
start_ts = date_to_milliseconds(data)
ETH = client.get_klines(symbol=symbol, interval=interval, startTime=start_ts)
prices = client.get_all_tickers()
for price in prices:
    if str(price['symbol']).__contains__('USDT'):
        print(price)

info = client.get_symbol_info('ETHUSDT')
print(info)