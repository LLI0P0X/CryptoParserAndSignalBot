import time
import asyncio
import aiohttp


async def getTime():
    return int(time.time() * 1000)


async def request1inchToUSDT(fromTokenAddress, toTokenAddress='0xdac17f958d2ee523a2206206994597c13d831ec7',
                             amount=5000000000, rev=False):
    walletAddress = '0x0000000000000000000000000000000000000000'
    # fromTokenAddress='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    # toTokenAddress='0xdac17f958d2ee523a2206206994597c13d831ec7' #USDT
    amount = str(amount)
    api = 1
    match toTokenAddress:
        case '0xdac17f958d2ee523a2206206994597c13d831ec7':
            api = 1
        case '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913':
            api = 8453
        case '0x55d398326f99059ff775485246999027b3197955':
            api = 56
        case '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9':
            api = 42161
        case '0x3c499c542cef5e3811e1192ce70d8cc03d5c3359':
            api = 137
        case '0x0b2c639c533813f4aa9d7837caf62653d097ff85':
            api = 10
        case '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7':
            api = 43114
    if rev:
        toTokenAddress, fromTokenAddress = fromTokenAddress, toTokenAddress
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://fusion.1inch.io/quoter/v1.1/{api}/quote/receive?walletAddress={walletAddress}&fromTokenAddress={fromTokenAddress}&toTokenAddress={toTokenAddress}&amount={amount}&enableEstimate=false') as resp:
            jsn = await resp.json()
            try:
                st = str(jsn['marketAmount'])
                fl = float(st)
                return fl
            except:
                return jsn


async def requestSolToUSDT(fromTokenAddress, toTokenAddress, amount, rev=False):
    async with aiohttp.ClientSession() as session:
        if rev:
            fromTokenAddress, toTokenAddress = toTokenAddress, fromTokenAddress
        async with session.get(
                f'https://quote-api.jup.ag/v6/quote?inputMint={fromTokenAddress}&outputMint={toTokenAddress}&amount={amount}&slippageBps=50&computeAutoSlippage=true&swapMode=ExactIn&onlyDirectRoutes=false&asLegacyTransaction=false&maxAccounts=64&experimentalDexes=Jupiter%20LO') as resp:
            jsn = await resp.json()
            try:
                st = str(jsn['outAmount'])
                fl = float(st)
                return fl
            except:
                return jsn


async def requestDexToUSDT(fromTokenAddress, toTokenAddress, amount, decimal):
    dusdt = 6
    if toTokenAddress == '0x55d398326f99059ff775485246999027b3197955':
        dusdt = 18
    amount = int(amount) * 10 ** dusdt
    decimal = int(decimal)

    if toTokenAddress == 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB':
        yR = await requestSolToUSDT(fromTokenAddress, toTokenAddress, amount, rev=True)
        try:
            xR = await requestSolToUSDT(fromTokenAddress, toTokenAddress, int(yR))
            x = xR / yR * 10 ** (decimal - dusdt)
            y = amount / yR * 10 ** (decimal - dusdt)
            return (x, y)
        except:
            return yR
    else:
        yR = await request1inchToUSDT(fromTokenAddress, toTokenAddress, amount, rev=True)
        try:
            xR = await request1inchToUSDT(fromTokenAddress, toTokenAddress, int(yR))
            x = xR / yR * 10 ** (decimal - dusdt)
            y = amount / yR * 10 ** (decimal - dusdt)
            return (x, y)
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
        async with session.get(
                f'https://www.okx.com/priapi/v5/market/trades?instId={name}-USDT&t={await getTime()}') as resp:
            jsn = await resp.json()
            try:
                f = 'sb'
                for q in jsn['data']:
                    if q['side'] == 'sell' and 's' in f:
                        s = q['px']
                        f = f.replace('s', '')
                    if q['side'] == 'buy' and 'b' in f:
                        b = q['px']
                        f = f.replace('b', '')
                    if f == '': break
                return float(s), float(b)
            except:
                return jsn


async def requestBybitToUSDT(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://api.bybit.com/spot/v3/public/quote/ticker/24hr?symbol={name}USDT') as resp:
            jsn = await resp.json()
            try:
                return float(jsn['result']['bp']), float(jsn['result']['ap'])
            except:
                return jsn


if __name__ == '__main__':
    print(asyncio.run(
        requestDexToUSDT('So11111111111111111111111111111111111111112', 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
                         1, 9)))
    # print(asyncio.run(requestBinanceToUSDT('ETH')))
    # print(asyncio.run(requestBybitToUSDT('ETH')))
    # print(asyncio.run(requestOkxToUSDT('ETH')))
    # print(asyncio.run(requestBybitToUSDT('ETH')))
