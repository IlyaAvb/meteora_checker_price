from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pyexpat.errors import messages

import meteora_add_lic

bot = Bot(token='7026287977:AAGjw7b6P-Jiv_e07U4cGNjbOeMhv3u-Pno')
dp = Dispatcher()


@dp.message(Command('start'))
async def start_message(message: types.Message):
    await message.answer(f'Привет {message.from_user.username}\n'
                         f'Буду присылать данные по пулу JLP - USDT каждые 30 секунд')
    await meteora_add_lic.main(message)

async def send_message(message, data):
    await message.answer(data)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())