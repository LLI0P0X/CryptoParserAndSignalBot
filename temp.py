import aiohttp
import asyncio
import requests
import secret

async def main():
    async with aiohttp.ClientSession() as sess:
        async with sess.get('https://ifconfig.me/ip', proxy=secret.proxy) as resp:
            print(await resp.text())

if __name__=='__main__':
    # r=requests.get('https://api.asocks.com/v2/proxy/ports?apikey=YxBwNdu8fyaHKRThvRG327L9M95QQFjY')
    # print(r.content)
    asyncio.run(main())