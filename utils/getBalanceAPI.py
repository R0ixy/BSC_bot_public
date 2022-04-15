import asyncio

import aiohttp

from data.config import APIKEY


async def get_price(session: aiohttp.ClientSession, coin: str, **kwargs):
    url = f"https://api.pancakeswap.info/api/v2/tokens/{coin}/"
    resp = await session.request('GET', url=url, **kwargs)
    data = await resp.json()
    coins = []
    if resp.status == 200:
        coins.append(data['data']['price'])
    else:
        coins.append(0)
    return coins


async def run_query(variables):
    # The GraphQL query
    query = """
    query ($address: String!) {
        ethereum(network: bsc) {
            address(address: {is: $address}) {
                balances {
                    currency {
                        address
                        symbol
                        tokenType
                    }
                    value
                }
            }
        }
    }
    """
    headers = {'X-API-KEY': APIKEY}
    async with aiohttp.ClientSession() as session:
        async with session.post('https://graphql.bitquery.io/',
                                json={'query': query, 'variables': variables}, headers=headers) as request:
            if request.status == 200:
                return await request.json()
            else:
                raise Exception('Query failed and return code is {}.      {}'.format(request.status,
                                                                                     query))


async def get_balance(address_data):
    variables = {'address': address_data['wallet']}
    result = await run_query(variables)  # Execute the query

    coins = []
    tokens = []
    total_value = float()
    try:
        for i in result['data']['ethereum']['address'][0]['balances']:
            if i['value'] != 0 and i['currency']['address'] == '-' and i['currency']['symbol'] == 'BNB':
                i['currency']['address'] = i['currency']['address'].replace('-',
                                                                            '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
            try:
                if i['currency']['address'] not in address_data['blacklist']:
                    tokens.append(i)
            except KeyError:
                tokens.append(i)
                # tokens.append(i['currency']['address'])
    except TypeError:
        return 1, 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        for c in tokens:
            tasks.append(get_price(session=session, coin=c['currency']['address']))
        prices = await asyncio.gather(*tasks, return_exceptions=True)


    # for i, price in zip(result['data']['ethereum']['address'][0]['balances'], prices):
    for i, price in zip(tokens, prices):
        if i['value'] != 0:

            if price == 0:
                coins.append(
                    ("<a href='https://bscscan.com/token/{address}'>{symbol}:</a> {value}"
                     "\nToken price: -"
                     "\nValue: -").format(address=i['currency']['address'], symbol=i['currency']['symbol'],
                                          value=i['value']))
            else:
                coins.append(
                    ("<a href='https://bscscan.com/token/{address}'>{symbol}:</a> {value}"
                     "\nToken price: {price}"
                     "\nValue: {usd_value}$").format(address=i['currency']['address'],
                                                     symbol=i['currency']['symbol'],
                                                     value=i['value'],
                                                     price=round(float(price[0]), 5),
                                                     usd_value=float(price[0]) * i['value']))

                total_value += round(float(price[0]) * i['value'], 3)

    return coins, total_value


async def get_all_tokens(address_data):
    variables = {'address': address_data['wallet']}
    result = await run_query(variables)  # Execute the query

    coins = []
    # tokens = []
    total_value = float()
    visible = []
    try:
        for i in result['data']['ethereum']['address'][0]['balances']:
            if i['value'] != 0 and i['currency']['address'] == '-' and i['currency']['symbol'] == 'BNB':
                i['currency']['address'] = i['currency']['address'].replace('-',
                                                                            '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
            # tokens.append(i['currency']['address'])
            try:
                if i['currency']['address'] in address_data['blacklist']:
                    visible.append(False)
                else:
                    visible.append(True)
            except KeyError:
                visible.append(True)
    except TypeError:
        return 1, 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        # for c in tokens:
        for c in result['data']['ethereum']['address'][0]['balances']:
            tasks.append(get_price(session=session, coin=c['currency']['address']))
        prices = await asyncio.gather(*tasks, return_exceptions=True)
    for i, price, visibility in zip(result['data']['ethereum']['address'][0]['balances'], prices, visible):
        if i['value'] != 0:

            if price == 0:
                coins.append(
                    {'data': ("<a href='https://bscscan.com/token/{address}'>{symbol}:</a> {value}"
                              "\nToken price: -"
                              "\nValue: -").format(address=i['currency']['address'],
                                                   symbol=i['currency']['symbol'],
                                                   value=i['value']),
                     'visibility': visibility})
            else:
                coins.append(
                    {'data': ("<a href='https://bscscan.com/token/{address}'>{symbol}:</a> {value}"
                              "\nToken price: {price}"
                              "\nValue: {usd_value}$").format(address=i['currency']['address'],
                                                              symbol=i['currency']['symbol'],
                                                              value=i['value'],
                                                              price=round(float(price[0]), 5),
                                                              usd_value=float(price[0]) * i['value']),
                     'visibility': visibility})

                total_value += round(float(price[0]) * i['value'], 3)

    return coins, total_value
