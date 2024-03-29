from aiogram import types, Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from requestsPrices import *
from funcsSQL import *

router = Router()

bot = Bot(token=config.BOT_TOKEN)


async def tryRequest(resp):
    match resp[2]:
        case "binance":
            cexl, cexh = await requestBinanceToUSDT(resp[1])
        case "mexc":
            cexl, cexh = await requestMexcToUSDT(resp[1])
        case "okx":
            cexl, cexh = await requestOkxToUSDT(resp[1])
        case "bybit":
            cexl, cexh = await requestBybitToUSDT(resp[1])

    print(cexl, cexh)

    dexl, dexh = await requestDexToUSDT(fromTokenAddress=resp[3], toTokenAddress=resp[4], amount=resp[6],
                                        decimal=resp[5])

    profitDC = (cexl - dexh) / dexh * 100
    profitCD = (dexl - cexh) / cexh * 100

    return f'{dexl}, {dexh}\n{cexl}, {cexh}\n{profitCD}, {profitDC}'


@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        await msg.answer("Добро пожаловать")
    else:
        await msg.answer("Ошибка авторизации")


@router.message(Command("create"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl = msg.text.split(' ')
        try:
            match msgl[4].lower():
                case 'eth':
                    msgl[4] = '0xdac17f958d2ee523a2206206994597c13d831ec7'
                case 'base':
                    msgl[4] = '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'
                case 'bsc':
                    msgl[4] = '0x55d398326f99059ff775485246999027b3197955'
                case 'arb':
                    msgl[4] = '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9'
                case 'polygon':
                    msgl[4] = '0x3c499c542cef5e3811e1192ce70d8cc03d5c3359'
                case 'optimism':
                    msgl[4] = '0x0b2c639c533813f4aa9d7837caf62653d097ff85'
                case 'avax':
                    msgl[4] = '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7'
                case 'sol':
                    msgl[4] = 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'
            resp = await tryRequest(msgl)

            await appendToTable(name=msgl[1], ex=msgl[2], from_add=msgl[3], to_add=msgl[4],
                                decimal=msgl[5], amount=msgl[6], need=msgl[7])
        except:
            resp = 'err'
        await msg.answer(str(resp))


@router.message(Command("show"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        sh = ''
        resp = await showTable()
        for st in resp:
            sh += f'{st[0]}||{st[15]}||{st[5]}$||{round(st[11], 2)}|{round(st[12], 2)}\n'
        if sh != '':
            await msg.answer(sh[:-1])
        else:
            await msg.answer('Нет отслеживаемых токенов ')


@router.message(Command("remove"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl = msg.text.split(' ')
        await removeFromTable(id=msgl[1])


@router.message(Command("edit_perc"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        msgl = msg.text.split(' ')
        await updateInTable(id=msgl[1], need=msgl[2])


@router.message(Command("help"))
async def start_handler(msg: Message):
    if msg.chat.id in config.users:
        await msg.answer(
            str('Введите /create [имя токена] [имя биржи] [адрес текена] [адрес usdt в выбранной сети] [decimals], [amount], [процент для сигнала]\nНапример:\n/create ETH bybit 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 0xdac17f958d2ee523a2206206994597c13d831ec7 18 1000000000000000000 0.01'))


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


@router.message(Command("timeout"))
async def start_handler(msg: Message):
    msgl = msg.text.split(' ')
    with open('timeout.txt', 'w') as f:
        f.write(msgl[1])


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
