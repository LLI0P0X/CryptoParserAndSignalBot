import datetime
import aiosqlite
import asyncio
import config


async def createTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        await db.execute(f'''CREATE TABLE {table} (
        id TEXT PRIMARY KEY,
        from_add TEXT,
        to_add TEXT, 
        name TEXT,
        decimal INTEGER,
        amount INTEGER,
        ex TEXT,
        dexl FLOAT,
        dexh FLOAT,
        cexl FLOAT,
        cexh FLOAT,
        dc FLOAT,
        cd FLOAT,
        time INTEGER,
        txt_time TEX,
        need FLOAT,
        ping BIT
        )''')
        await db.commit()

        async with db.execute(f'SELECT * FROM {table}') as cursor:
            return await cursor.fetchall()


async def appendToTable(database=config.pathToBd + 'data.db', table='customPreset',
                        name='ETH',
                        ex='bybit',
                        from_add='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                        to_add='0xdac17f958d2ee523a2206206994597c13d831ec7',
                        decimal=18,
                        amount=5000,
                        need=0.01
                        ):
    net = 'err'
    match to_add:
        case '0xdac17f958d2ee523a2206206994597c13d831ec7':
            net = 'eth'
        case '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913':
            net = 'base'
        case '0x55d398326f99059ff775485246999027b3197955':
            net = 'bsc'
        case '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9':
            net = 'arb'
        case '0x3c499c542cef5e3811e1192ce70d8cc03d5c3359':
            net = 'polygon'
        case '0x0b2c639c533813f4aa9d7837caf62653d097ff85':
            net = 'optimism'
        case '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7':
            net = 'avax'
    params = (
        f'{name}_{ex}_{net}',
        from_add,
        to_add,
        name,
        int(decimal),
        int(amount),
        ex,
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        1,
        '1',
        float(need),
        0
    )
    async with aiosqlite.connect(database) as db:
        await db.execute(f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', params)
        await db.commit()

        async with db.execute(f'SELECT * FROM {table}') as cursor:
            return await cursor.fetchall()


async def showTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f'SELECT * FROM {table}') as cursor:
            return await cursor.fetchall()


async def needUpdateInTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f'SELECT * FROM {table} WHERE time != 0 ORDER BY time') as cursor:
            return await cursor.fetchall()


async def updateInTable(id, database=config.pathToBd + 'data.db', table='customPreset', dexl=None, dexh=None, cexl=None,
                        cexh=None,
                        dc=None, cd=None, time=None, txt_time=None, need=None, ping=None):
    args = {'dexl': dexl,
            'dexh': dexh,
            'cexl': cexl,
            'cexh': cexh,
            'dc': dc,
            'cd': cd,
            'time': time,
            'txt_time': txt_time,
            'need': need,
            'ping': ping}
    params = []
    query = f'UPDATE {table} SET'
    for arg in args:
        if args[arg] is not None:
            query += f' {arg} = ?,'
            params.append(args[arg])
    params.append(id)
    query = query[:-1] + ' WHERE id = ?'
    print(query, params)
    async with aiosqlite.connect(database) as db:
        await db.execute(query, params)
        await db.commit()
        async with db.execute(f'SELECT * FROM {table} WHERE id = ?', [id]) as cursor:
            return await cursor.fetchall()


async def removeTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        await db.execute(f'DROP TABLE {table}')
        await db.commit()


async def removeFromTable(id, database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        await db.execute(f'DELETE FROM {table} WHERE id = ?', [id])
        await db.commit()


async def starterForTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        await db.execute(f'UPDATE {table} SET time=1')
        await db.commit()


async def findByID(id, database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f'SELECT * FROM {table} WHERE id = ?', [id]) as cursor:
            return await cursor.fetchall()


async def pingsFromTable(database=config.pathToBd + 'data.db', table='customPreset'):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f'SELECT * FROM {table} WHERE ping > ?', [0]) as cursor:
            return await cursor.fetchall()


async def main():
    try:
        temp = await showTable()
        await removeTable()
        for st in temp:
            print(st)
    except:
        print('cl')
    print('---start---')
    await createTable()
    await appendToTable()
    await appendToTable(name='TOKEN', ex='bybit', from_add='0x4507cEf57C46789eF8d1a19EA45f4216bae2B528',
                        to_add='0xdAC17F958D2ee523a2206206994597C13D831ec7', decimal=9, amount=5000,
                        need=0.01)
    temp = await showTable()
    for st in temp:
        print(st)


if __name__ == '__main__':
    asyncio.run(updateInTable(id='ETH_bybit_eth', txt_time=str(datetime.datetime.now())))
    # asyncio.run(main())
