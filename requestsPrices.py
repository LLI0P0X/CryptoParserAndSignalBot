import requests
import json
import time
import datetime
import asyncio
import aiohttp

async def getTime():
    return int(time.time()*1000)

async def request1inchToUSDTBuy(fromTokenAddress, toTokenAddress='0xdac17f958d2ee523a2206206994597c13d831ec7', amount=5000000000, rev=False):
    walletAddress = '0x0000000000000000000000000000000000000000'
    # fromTokenAddress='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    # toTokenAddress='0xdac17f958d2ee523a2206206994597c13d831ec7' #USDT
    amount=str(amount)
    if rev:
        toTokenAddress, fromTokenAddress = fromTokenAddress, toTokenAddress
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://fusion.1inch.io/quoter/v1.1/1/quote/receive?walletAddress={walletAddress}&fromTokenAddress={fromTokenAddress}&toTokenAddress={toTokenAddress}&amount={amount}&enableEstimate=false') as resp:
            jsn = await resp.json()
            try:
                st=str(jsn['marketAmount'])
                # fl=float(st[:-6]+'.'+st[-6:])
                fl = float(st)
                return fl
            except:
                return jsn

async def request1inchToUSDT(fromTokenAddress, toTokenAddress, amount, decimal):
    amount = int(amount)*10**6
    decimal = int(decimal)
    yR = await request1inchToUSDTBuy(fromTokenAddress, toTokenAddress, amount, rev=True)
    try:
        xR = await request1inchToUSDTBuy(fromTokenAddress, toTokenAddress, int(yR))
        x = xR/yR*10**(decimal-6)
        y = amount/yR*10**(decimal-6)
        return (x,y)
    except:
        return yR

async def requestBinanceToUSDT(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.binance.com/api/v3/depth?symbol={name}USDT&limit=1') as resp:
            jsn = await resp.json()
            return float(jsn["bids"][0][0]), float(jsn["asks"][0][0])
            # return jsn

async def requestMexcToUSDT(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.mexc.com/api/platform/market/spot/depth?symbol={name}_USDT') as resp:
            jsn = await resp.json()
            try:
                return float(jsn["data"]["data"]['bids'][0]['p']), float(jsn["data"]["data"]['asks'][0]['p'])
            except:
                return jsn

async def requestOkxToUSDT(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.okx.com/priapi/v5/market/trades?instId={name}-USDT&t={await getTime()}') as resp:
            jsn = await resp.json()
            try:
                f='sb'
                for q in jsn['data']:
                    if q['side'] == 'sell' and 's' in f:
                        s = q['px']
                        f=f.replace('s','')
                    if q['side'] == 'buy' and 'b' in f:
                        b = q['px']
                        f=f.replace('b','')
                    if f=='': break
                return float(s), float(b)
            except:
                return jsn

        # async with session.get(f'https://www.okx.com/api/v5/public/price-limit?instId={name}-USDT-SWAP') as resp:
        #     jsn = await resp.json()
        #     try:
        #         return float(jsn['data'][0]['sellLmt']), float(jsn['data'][0]['buyLmt'])
        #     except:
        #         return jsn

async def requestBybitToUSDT(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api-testnet.bybit.com/v5/market/tickers?category=inverse&symbol={name}USDT') as resp:
            jsn = await resp.json()
            return float(jsn['result']['list'][0]['bid1Price']), float(jsn['result']['list'][0]['ask1Price'])
            # return json.dumps(jsn,indent=4)

if __name__ == '__main__':
    # print(asyncio.run(request1inchToUSDT('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xdac17f958d2ee523a2206206994597c13d831ec7', 5000, 18)))
    # print(asyncio.run(requestBinanceToUSDT('ETH')))
    # print(asyncio.run(requestBybitToUSDT('TOKEN')))
    print(asyncio.run(requestOkxToUSDT('ETH')))
    # print(asyncio.run(requestBybitToUSDT('ETH')))
# (3522.111763, 3522.7738112502766)
