from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

TOKEN = os.getenv("TOKEN")

COINS = ["ZROUSDT", "MEMEUSDT","ZKUSDT","APTUSDT","SANDUSDT"]
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

COL_MONET = {
    "ZROUSDT": 1111,
    "MEMEUSDT": 111,
    "ZKUSDT": 1111,
    "APTUSDT": 1111,
    "SANDUSDT": 11111
}


async def feth_prices(symbol: list[str]) -> list[tuple[str, float]]:
    async with httpx.AsyncClient(timeout= 10.0) as client:
        tasks = [client.get(BINANCE_URL,params={"symbol": s}) for s in symbol]
        response = await asyncio.gather(*tasks)
    out: list[tuple[str,float]] = []
    for r in response:
        r.raise_for_status()
        data = r.json()
        out.append((data["symbol"],data["price"]))
    return out

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher

    @dp.message(lambda m: m.text == "+")
    async def show_prices(message: types.Message):
        prices = await feth_prices(COINS)
        
        current_total = sum(COL_MONET[symbol] * price for symbol,price in prices if symbol in COINS)
        
        target_sum = 10000
        
        growth_percent = ((target_sum - current_total) / current_total) * 100
        
        text = "\n".join(f"{symbol}: {price:.2f} USDT" for symbol, price in prices)
        text += f"\n\n SELL ALL {growth_percent:.2f}"
        
        await message.answer(text)
        
    await dp.start_polling(bot)
        
        
if __name__ == "__main__":
    asyncio.run(main())
        
    









        
        
