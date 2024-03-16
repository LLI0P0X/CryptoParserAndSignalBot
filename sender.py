from aiogram.utils.keyboard import InlineKeyboardBuilder
from funcsSQL import *
from aiogram import Bot, types
import config
import asyncio

bot = Bot(token=config.BOT_TOKEN)


async def pinger(resp):
    msg = ''
    builder = InlineKeyboardBuilder()
    for st in resp:
        name = st[3]
        value = st[5]
        ex = st[6]
        if st[2] == 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB':
            dex = 'jup'
        else:
            dex = '1inch'
        if not (st[11] > st[15] or st[12] > st[15]):
            return None
        if st[11] > st[15]:
            ex1 = dex
            price1 = st[8]
            ex2 = st[6]
            price2 = st[9]
            profit = st[11]
            msg += f'{name} ({st[0].split("_")[-1]}) | {ex} | {value} USDT | {round(profit, 2)} \n\n'
            msg += f'buy {ex1} {price1}\nsell {ex2} {price2}\n\n{round(profit, 2)}%\n\n--------\n\n'
        if st[12] > st[15]:
            ex2 = dex
            price2 = st[7]
            ex1 = st[6]
            price1 = st[10]
            profit = st[12]
            msg += f'{name} ({st[0].split("_")[-1]}) | {ex} | {value} USDT | {round(profit, 2)} \n\n'
            msg += f'buy {ex1} {price1}\nsell {ex2} {price2}\n\n{round(profit, 2)}%\n\n--------\n\n'
        msg += f'`{st[1]}`\n'
        msg += f'`/edit_perc {st[0]} `\n'
        msg += '--------\n\n'
        builder.add(types.InlineKeyboardButton(
            text=f"Удалить {st[0]}",
            callback_data=f"remove {st[0]}")
        )
    msg = msg[:-1]
    for id in config.sendTo:
        await bot.send_message(id, msg, reply_markup=builder.as_markup(), parse_mode="MARKDOWN")


async def autoPinger():
    temp = await showTable()
    if temp != []:
        await starterForTable()
    for st in temp:
        print(st)
    print('----run----')
    while True:
        resp = await pingsFromTable()
        if resp == []:
            print(f'{datetime.datetime.now()} sleep')
            await asyncio.sleep(1)
            continue
        asyncio.ensure_future(pinger(resp))
        try:
            with open('timeout.txt', 'r') as f:
                timeout = int(f.read())
        except:
            timeout = config.timeout
        print(timeout)
        await asyncio.sleep(timeout)


asyncio.run(autoPinger())
