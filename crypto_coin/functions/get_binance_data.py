import sys
from concurrent.futures import thread

from binance.client import Client
import pytz, dateparser
from datetime import datetime
from pycoingecko import CoinGeckoAPI


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


def get_all_cryptodata():
    client = Client("", "")
    symbol = "ETHUSDT"
    year = datetime.now().year
    interval = Client.KLINE_INTERVAL_1DAY
    m = datetime.now().month
    day = datetime.now().day
    data_out = []

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
            price['price'] = format(float(price['price']), '.2f')
            data_out.append(price)
    return data_out


def CoinGeckoGet():
    cg = CoinGeckoAPI()
    id = cg.get_coins_list()
    return id


def market_cap(ids):
    cg = CoinGeckoAPI()
    return cg.get_price(ids=ids, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true')


def get_all_crypto_info():
    coins = CoinGeckoGet()
    data_cryptodata = get_all_cryptodata()

    symbol = []
    cryptocurrency = []

    for coin in data_cryptodata:
        symbol.append(str(coin['symbol']).replace("USDT", "").lower())
        coin['symbol'] = str(coin['symbol']).replace("USDT", "").lower()

    for sym in symbol:
        for coin in coins:
            if sym == coin['symbol']:
                cryptocurrency.append(coin)

    CRYPTO_DATA2 = []
    for coin_gecko in cryptocurrency:
        for coin_binance in data_cryptodata:
            if coin_binance['symbol'] == coin_gecko['symbol']:
                coin_binance['name'] = coin_gecko['name']
                coin_binance['id'] = coin_gecko['id']
                CRYPTO_DATA2.append(coin_binance)

    seen = set()
    CRYPTO_DATA = []
    for d in CRYPTO_DATA2:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            CRYPTO_DATA.append(d)

    list_id = []
    for coiny in CRYPTO_DATA:
        if 'binance-vnd' != coiny['id']:
            list_id.append(coiny['id'])

    market_cap_list = market_cap(list_id)
    keys_list = market_cap_list.keys()

    data_crypto_out = []
    for key in keys_list:
        for coin_crypto_data in CRYPTO_DATA:
            if key == coin_crypto_data['id']:
                coin_crypto_data['usd_market_cap'] = market_cap_list[key]['usd_market_cap']
                coin_crypto_data['usd_24h_vol'] = market_cap_list[key]['usd_24h_vol']
                data_crypto_out.append(coin_crypto_data)
    return data_crypto_out


def update_db_crypto_coin():
    get_crypto_info = get_all_crypto_info()
    return get_crypto_info
