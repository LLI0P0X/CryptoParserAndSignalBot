from funcsSQL import *
from requestsPrices import *
import datetime


async def starter():
    try:
        return await createTable()
    except:
        return await showTable()


async def autoRequest(resp):
    cexl, cexh = 0, 0
    match resp[6]:
        case "binance":
            cexl, cexh = await requestBinanceToUSDT(resp[3])
        case "mexc":
            cexl, cexh = await requestMexcToUSDT(resp[3])
        case "okx":
            cexl, cexh = await requestOkxToUSDT(resp[3])
        case "bybit":
            cexl, cexh = await requestBybitToUSDT(resp[3])

    dexl, dexh = await requestDexToUSDT(fromTokenAddress=resp[1], toTokenAddress=resp[2], amount=resp[5],
                                        decimal=resp[4])

    profitCD = (dexl - cexh) / dexh * 100
    profitDC = (cexl - dexh) / cexh * 100

    t = await getTime()
    ping = int(profitCD > resp[15] or profitDC > resp[15])
    await updateInTable(id=resp[0], dexh=dexh, dexl=dexl, cexh=cexh, cexl=cexl, dc=profitDC, cd=profitCD, time=t,
                        txt_time=str(datetime.datetime.now()), ping=ping)


async def autoRequester(resp):
    await updateInTable(id=resp[0], time=0)
    try:
        await autoRequest(resp)
    except:
        await updateInTable(id=resp[0], time=1)


async def main():
    await starter()
    temp = await showTable()
    if temp != []:
        await starterForTable()
    for st in temp:
        print(st)
    print('----run----')
    while True:
        resp = await needUpdateInTable()
        if resp == []:
            await asyncio.sleep(1)
            continue
        asyncio.ensure_future(autoRequester(resp[0]))
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(main())
