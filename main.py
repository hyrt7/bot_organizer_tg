from aiogram import Bot, executor, Dispatcher, types


TOKEN = '6178466838:AAEeX_CBrb7JQiHkSVVcp2skI9AkEKnQqW8'
HELP = '''/help - список команд
/start - начать работу с ботом
/plan - сделать прогноз погоды'''

bot = Bot(TOKEN)
dp = Dispatcher(bot)
async def on_startup(_):
    print('Бот запущен')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}, добро пожаловать в наш Телеграмм Бот!')
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEIAbFkBHf3USGmNpL6XU28yDBbKGBuiAACvQwAAgbX6UmiQ5zoyiNTgS4E')
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)