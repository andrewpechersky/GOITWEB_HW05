import asyncio
import aiohttp
import pprint
import sys
from datetime import datetime, timedelta


API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


async def fetch_currency_rates(session, date):
    url = f"{API_URL}{date}"
    #
    async with session.get(url) as response:
        data = await response.json()  # upd
        return data


def get_currency_rates(data):
    rates = {}
    for i in data['exchangeRate']:

        if i['currency'] in ('EUR', 'USD'):
            rates[i['currency']] = {
                'sale': i['saleRateNB'],
                'purchase': i['purchaseRateNB']
            }
    return rates


async def get_recent_rates(count_of_days):
    async with aiohttp.ClientSession() as session:
        today = datetime.now()
        recent_rates = []
        for i in range(count_of_days):
            date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            data = await fetch_currency_rates(session, date)
            rates = get_currency_rates(data)
            for currency, rate in rates.items():
                recent_rates.append({date: {currency: rate}})
        return recent_rates

if __name__ == "__main__":
    try:
        count_of_days = int(sys.argv[1])
        if count_of_days > 10:
            raise ValueError("Count of days can be < 10")
    except IndexError:
        print("You have to enter count of days as an argument")
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)

    loop = asyncio.get_event_loop()
    recent_rates = loop.run_until_complete(get_recent_rates(count_of_days))
    pprint.pprint(recent_rates)
