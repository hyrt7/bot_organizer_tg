import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ContentType
from aiogram.utils import executor


TOKEN = '5669197589:AAF7IgMXN6g5LV-3kSiUV3tHaDLV9T6ET_A'

menu_veganfood = '''Завтрак:
- Овсянка на воде с фруктами и орехами
- Тост из цельнозернового хлеба с авокадо и овощами
- Фруктовый смузи с бананом и миндальным молоком

Перекус:
- Фруктовый салат с орехами
- Хумус с овощами

Обед:
- Тофу с овощами на гриле
- Курица из соевых белков с овощами
- Овощной суп с кускусом

Полдник:
- Фруктовый салат с орехами
- Тост из цельнозернового хлеба с авокадо и овощами

Ужин:
- Фаршированный перец с овощами и рисом
- Картофельное пюре с овощами и соусом из орехов
- Салат из томатов, огурцов и авокадо

Перед сном:
- Банан
- Коктейль из миндального молока с медом

Важно помнить, что порции должны быть не слишком большими, а калорийность питания должна соответствовать уровню активности спортсмена. Также следует учитывать индивидуальные особенности организма и консультироваться с диетологом.
'''

menu_food = '''Завтрак:
- Овсянка на молоке с фруктами и орехами
- Яйца пашот с тостом из цельнозернового хлеба
- Фруктовый смузи с йогуртом

Перекус:
- Смесь орехов и сухофруктов
- Творог с ягодами

Обед:
- Гриль из куриной грудки с овощами
- Рыба на пару с овощами
- Овощной салат с кускусом и курицей

Полдник:
- Яблоко с миндальным маслом
- Тост из цельнозернового хлеба с авокадо и тунцом

Ужин:
- Фаршированный перец с рисом и овощами
- Говядина на гриле с картофелем и овощами
- Салат из ростбифа с овощами

Перед сном:
- Банан
- Коктейль из кефира с медом'''

exercizes_1 = '''Тренировка 1 (легкая):
- Бег: 5 минут замедленного бега + 10 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 10 отжиманий на коленях
- Приседания: 3 подхода по 10 приседаний без веса'''

exercizes_2 = '''Тренировка 2 (средняя):
- Бег: 10 минут замедленного бега + 20 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 15 отжиманий на коленях
- Приседания: 3 подхода по 15 приседаний со средним весом (гантели или бутылки с водой)'''

exercizes_3 = '''Тренировка 3 (сложная):
- Бег: 10 минут замедленного бега + 30 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 20 отжиманий на полной амплитуде
- Приседания: 3 подхода по 20 приседаний со значительным весом (гантели или бутылки с песком)'''


# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и хранилище состояний
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создаем состояния для FSM
class UserState(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    activity_level = State()
    goal = State()

# Создаем клавиатуру
menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu.add(KeyboardButton(text='Упражнения'))
menu.add(KeyboardButton(text='Питание'))
menu.add(KeyboardButton(text='Цель'))


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Отправляем приветственное сообщение и предлагаем пройти опрос

    global user_id
    user_id = message.from_user.id
    await message.answer(text=f'Привет, {message.from_user.full_name}, добро пожаловать в нашего Телеграмм Ботa! Пройдите опрос для ледущей работы. Ваш пол:', reply_markup=menu)
    await bot.send_sticker(user_id, sticker='CAACAgIAAxkBAAEIAbFkBHf3USGmNpL6XU28yDBbKGBuiAACvQwAAgbX6UmiQ5zoyiNTgS4E')

    # Устанавливаем состояние gender
    await UserState.gender.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.gender)
async def process_gender(message: types.Message, state: FSMContext):
    # Сохраняем пол пользователя
    async with state.proxy() as data:
        data['gender'] = message.text

    # Просим пользователя ввести возраст
    await message.answer('Введите ваш возраст:')

    # Устанавливаем состояние age
    await UserState.age.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    # Сохраняем возраст пользователя
    async with state.proxy() as data:
        data['age'] = message.text

    # Просим пользователя ввести рост
    await message.answer('Введите рост:')

    # Устанавливаем состояние height
    await UserState.height.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.height)
async def process_height(message: types.Message, state: FSMContext):
    # Сохраняем рост пользователя
    async with state.proxy() as data:
        data['height'] = message.text

    # Просим пользователя ввести вес
    await message.answer('Введите ваш вес:')

    # Устанавливаем состояние weight
    await UserState.weight.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.weight)
async def process_weight(message: types.Message, state: FSMContext):
    # Сохраняем вес пользователя
    async with state.proxy() as data:
        data['weight'] = message.text

    # Просим пользователя выбрать уровень активности
    await message.answer('Выберите уровень активности:', reply_markup=types.ReplyKeyboardRemove())

    # Устанавливаем состояние activity_level
    await UserState.activity_level.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.activity_level)
async def process_activity(message: types.Message, state: FSMContext):
    # Сохраняем уровень активности пользователя
    async with state.proxy() as data:
        data['activity_level'] = message.text
    await message.answer('Введите цель своих занятий:')

    # Устанавливаем состояние goal
    await UserState.goal.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.goal)
async def process_goal(message: types.Message, state: FSMContext):
    # Сохраняем цель пользователя
    async with state.proxy() as data:
        data['goal'] = message.text

    # Поздравляем пользователя с завершением опроса и предлагаем начать обучение
    await message.answer('Спасибо за прохождение опроса! Подгототавливаю список упражнений.', reply_markup=menu)

    # Сбрасываем состояние
    await state.finish()

# Обработчик кнопки "Упражнения"
@dp.message_handler(text='Упражнения')
async def process_exercises(message: types.Message):
    # Отправляем пользователю список упражнений
    await message.answer('список')

# Обработчик кнопки "Питание"
@dp.message_handler(text='Питание')
async def process_nutrition(message: types.Message):
    # Отправляем пользователю советы по здоровому питанию
    menu.add()
    await message.answer('Советы по питанию')

# Обработчик кнопки "Цель"
@dp.message_handler(text='Цель')
async def process_goal_button(message: types.Message):
    # Отправляем пользователю информацию о его цели
    await message.answer('Советы по цели')


import asyncio

# Функция для напоминания о тренировке
async def remind_about_exercises():
    while True:
        # Отправляем сообщение о тренировке
        await bot.send_message(chat_id=user_id, text='Пора тренироваться!')

        # Ждем 24 часа
        await asyncio.sleep(24 * 60 * 60)

# Функция для напоминания о цели
async def remind_about_goal():
    while True:
        # Отправляем сообщение о цели
        await bot.send_message(chat_id=user_id, text=UserState.goal)

        # Ждем неделю
        await asyncio.sleep(10)


if __name__ == '__main__':
    # Запускаем задачи
    loop = asyncio.get_event_loop()
    loop.create_task(remind_about_exercises())
    loop.create_task(remind_about_goal())

    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
