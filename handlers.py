import aiogram
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from funcsSQL import appendToTable

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

import config

from requestsPrices import *
from funcsSQL import *

import asyncio

router = Router()

bot = Bot(token=config.BOT_TOKEN)

async def tryRequest(resp):
    match resp[2]:
        case "binance": cexl, cexh = await requestBinanceToUSDT(resp[1])
        case "mexc": cexl, cexh = await requestMexcToUSDT(resp[1])
        case "okx": cexl, cexh = await requestOkxToUSDT(resp[1])
        case "bybit": cexl, cexh = await requestBybitToUSDT(resp[1])
    dexl, dexh = await request1inchToUSDT(fromTokenAddress=resp[3], toTokenAddress=resp[4], amount=resp[6], decimal=resp[5])
    profitDC = (cexl - dexh) / dexh * 100
    profitCD = (dexl - cexh) / cexh * 100


    # print(dexl, dexh)
    # print(cexl, cexh)
    # print(profitCD, profitDC)

    return f'{dexl}, {dexh}\n{cexl}, {cexh}\n{profitCD}, {profitDC}'

@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        await msg.answer("Добро подаловать")
    else:
        await msg.answer("Ошибка авторизации")

@router.message(Command("create"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl = msg.text.split(' ')
        try:
            match msgl[4].lower():
                case 'base':
                    msgl[4] = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
                case 'eth':
                    msgl[4] = '0xdac17f958d2ee523a2206206994597c13d831ec7'
                case 'bsc':
                    msgl[4] = '0x55d398326f99059ff775485246999027b3197955'
                case 'arb':
                    msgl[4] = '0x2791bca1f2de4661ed88a30c99a7a9449aa84174'
                case 'polygon':
                    msgl[4] = '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85'
                case 'optimism':
                    msgl[4] = '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9'
                case 'avax':
                    msgl[4] = '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7'

            resp = await tryRequest(msgl)

            await appendToTable(name=msgl[1], ex=msgl[2], from_add=msgl[3], to_add=msgl[4],
                            decimal=msgl[5],amount=msgl[6],need=msgl[7])
        except:
            resp='err'
        await msg.answer(str(resp))

@router.message(Command("show"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        sh=''
        resp = await showTable()
        for st in resp:
            sh+=f'{st[0]}||{st[15]}||{round(st[11],2)}|{round(st[12],2)}\n'
        if sh!='': await msg.answer(sh[:-1])
        else: await msg.answer('Нет отслеживаемых токенов ')


@router.message(Command("remove"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl=msg.text.split(' ')
        await removeFromTable(id=msgl[1])

@router.message(Command("edit_perc"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl=msg.text.split(' ')
        await updateInTable(id=msgl[1], need=msgl[2])

@router.message(Command("help"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        await msg.answer(str('Введите /create [имя токена] [имя биржи] [адрес текена] [адрес usdt в выбранной сети] [decimals], [amount], [процент для сигнала]\nНапример:\n/create ETH bybit 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 0xdac17f958d2ee523a2206206994597c13d831ec7 18 1000000000000000000 0.01'))

# /req 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 0xdac17f958d2ee523a2206206994597c13d831ec7 ETH 18 1000000000000000000 bybit
@router.message(Command("req"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        try:
            r = await tryRequest(str(msg.text).split(' '))
            print(r)
        except Exception as err:
            print(err)
            r = 'err'
        await msg.answer(r)

@router.message(Command("find"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        temp = msg.text.split(' ')
        try:
            resp = await findByID(f'{temp[1]}')
            r = resp[0]
            ans = f'{r[7]}, {r[8]}\n{r[9]}, {r[10]}\n{r[11]}, {r[12]}'
            await msg.answer(str(ans))
        except:
            await msg.answer('err')

@router.callback_query(lambda c: "remove" in c.data)
async def send_random_value(callback: types.CallbackQuery):
    msgl = str(callback.data).split(' ')
    await removeFromTable(id=msgl[1])
