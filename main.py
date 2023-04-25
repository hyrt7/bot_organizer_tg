import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

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

exercizes_1 = '''Активность 1 (легкая):
- Бег: 5 минут замедленного бега + 10 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 10 отжиманий на коленях
- Приседания: 3 подхода по 10 приседаний без веса'''

exercizes_2 ='''Активность 2 (средняя):
- Бег: 10 минут замедленного бега + 20 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 15 отжиманий на коленях
- Приседания: 3 подхода по 15 приседаний со средним весом (гантели или бутылки с водой)'''

exercizes_3 = '''Активность 3 (сложная):
- Бег: 10 минут замедленного бега + 30 минут бега на среднем темпе + 5 минут ходьбы для охлаждения
- Отжимания: 3 подхода по 20 отжиманий на полной амплитуде
- Приседания: 3 подхода по 20 приседаний со значительным весом (гантели или бутылки с песком)'''

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
menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
menu.add(KeyboardButton(text='Упражнения'))
menu.add(KeyboardButton(text='Питание'))
menu.add(KeyboardButton(text='Цель'))

opros_sex = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
opros_sex.add(KeyboardButton(text='Мужской'))
opros_sex.add(KeyboardButton(text='Женский'))
opros_sex.add(KeyboardButton(text='Другой'))

opros_activity = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
opros_activity.add(KeyboardButton(text='1 (легкая)'))
opros_activity.add(KeyboardButton(text='2 (средняя)'))
opros_activity.add(KeyboardButton(text='3 (сложная)'))

food = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
food.add(KeyboardButton(text='Примерное меню для обычного спорстмена'))
food.add(KeyboardButton(text='Примерное меню для спортсмена вегана'))

goal_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
goal_kb.add(KeyboardButton(text='Подкачаться'))
goal_kb.add(KeyboardButton(text='Похудеть'))
goal_kb.add(KeyboardButton(text='Чтобы стало 10 кубиков на прессе)))))'))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Отправляем приветственное сообщение и предлагаем пройти опрос
    global user_id
    user_id = message.from_user.id
    await message.answer(text=f'Привет, {message.from_user.full_name}, добро пожаловать в нашего Телеграмм Ботa! Пройдите опрос для следущей работы. Ваш пол:', reply_markup=opros_sex)
    await bot.send_sticker(user_id, sticker='CAACAgIAAxkBAAEIAbFkBHf3USGmNpL6XU28yDBbKGBuiAACvQwAAgbX6UmiQ5zoyiNTgS4E',)

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
    await message.answer('Выберите уровень активности:', reply_markup=opros_activity)

    # Устанавливаем состояние activity_level
    await UserState.activity_level.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=UserState.activity_level)
async def process_activity(message: types.Message, state: FSMContext):
    # Сохраняем уровень активности пользователя
    async with state.proxy() as data:
        data['activity_level'] = message.text
    global activity_level
    activity_level = message.text
    await message.answer('Спасибо за прохождение опроса! Подгототавливаю список упражнений. Пожалуйста, установите цель или цели используя /goal', reply_markup=menu)

    # Сбрасываем состояние
    await state.finish()

# Обработчик кнопки "Упражнения"
@dp.message_handler(text='Упражнения')
async def process_exercises(message: types.Message, state: FSMContext):
    # Отправляем пользователю список упражнений
    result = cursor.execute(f'''SELECT activity_level FROM log_entries_1 WHERE user_id = {message.from_user.id}''').fetchall()
    if result[0][0][0] == '1':
        await message.answer(exercizes_1)
    elif result[0][0][0] == '2':
        await message.answer(exercizes_2)
    elif result[0][0][0] == '3':
        await message.answer(exercizes_3)

# Обработчик кнопки "Питание"
@dp.message_handler(text='Питание')
async def process_nutrition(message: types.Message):
    # Отправляем пользователю советы по здоровому питанию
    menu.add()
    await message.answer('''1. Питайтесь разнообразно и сбалансированно, употребляйте продукты всех групп пищевых веществ, таких как белки, углеводы и жиры.

2. Ограничьте потребление продуктов, содержащих большое количество животных жиров, холестерина, сахара, соли и пустых углеводов.

3. Употребляйте меньшие порции еды, но чаще - 5-6 раз в день. 

4. Увеличьте потребление овощей, фруктов, ягод, злаковых продуктов, бобовых и орехов.

5. Пейте достаточное количество воды - от 1,5 до 2 литров в день.

6. Избегайте переедания, ешьте медленно и жуйте пищу тщательно.

7. Придерживайтесь правильного режима питания, не пропускайте завтрак и ужинайте за 2-3 часа до сна.

8. Избегайте употребления алкоголя и курения.''', reply_markup=food)

@dp.message_handler(text='Примерное меню для обычного спорстмена')
async def food_for_sport(message: types.Message):
    await message.reply(menu_food, reply_markup=menu)

@dp.message_handler(text='Примерное меню для спортсмена вегана')
async def food_for_sport(message: types.Message):
    await message.reply(menu_veganfood,reply_markup=menu)

# Обработчик кнопки "Цель"
@dp.message_handler(text='Цель')
async def process_goal_button(message: types.Message):
    # Отправляем пользователю информацию о его цели
    result = cursor.execute(f'''SELECT entry FROM log_entries_1 WHERE user_id = {message.from_user.id}''').fetchall()
    await message.answer(f'''Ваша цель - {result[0][0]}
    Я помогу вам с мотивацией:\n\" Я скажу то, что для тебя не новость: мир не такой уж солнечный и приветливый. Это очень опасное, жесткое место, и если только дашь слабину, он опрокинет с такой силой тебя, что больше уже не встанешь. Ни ты, ни я, никто на свете, не бьёт так сильно, как жизнь! Совсем не важно, как ты ударишь, а важно, какой держишь удар, как двигаешься вперёд. Будешь идти — ИДИ! Если с испугу не свернёшь... Только так побеждают! Если знаешь, чего ты стоишь — иди и бери своё!\" - Рокки Бальбоа''')



import sqlite3

# созда подключениение к базе данных
conn = sqlite3.connect('health_bot.db')
cursor = conn.cursor()

# создание таблицы для хранения журнала достижений
cursor.execute('''CREATE TABLE IF NOT EXISTS log_entries_1
                  (user_id INTEGER, entry TEXT, activity_level TEXT, date TEXT)''')
conn.commit()

# функция для добавления записи в журнал достижений
def add_log_entry(user_id, entry, activity_level):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO log_entries_1 VALUES (?, ?, ?, ?)", (user_id, entry,activity_level, date))
    conn.commit()

@dp.message_handler(commands=['goal'])
async def achievments(message: types.Message):
    await message.reply("Что ты хочешь записать в свою цель?",reply_markup=goal_kb)
    # добавьте обработчик ответа пользователя
    dp.register_message_handler(log_entry)


# создание функции для записи достижений
async def log_entry(message: types.Message):
    user_id = message.from_user.id
    entry = message.text
    add_log_entry(user_id, entry,activity_level)  # добавить запись в базу данных
    await message.answer(text='Цель успешно было добавлена!', reply_markup=menu)

# Функция для напоминания о тренировке
async def remind_about_exercises():
    while True:
        # Отправляем сообщение о тренировке
        result = cursor.execute(f'''SELECT user_id FROM log_entries_1''').fetchall()
        for i in result:
            await bot.send_message(chat_id=i[0], text='Пора тренироваться!')

        # Ждем 24 часа, можете поставить меньше если хотите проверить
        await asyncio.sleep(24*60*60)

# Функция для напоминания о цели
async def remind_about_goal():
    while True:
        # Отправляем сообщение о цели
        result = cursor.execute(f'''SELECT user_id FROM log_entries_1''').fetchall()
        for i in result:
            result = cursor.execute(f'''SELECT entry FROM log_entries_1 WHERE user_id = {i[0]}''').fetchall()
            await bot.send_message(chat_id=i[0], text=f'Твоя цель - {result[0][0]}, не забывай про нее!')

        # Ждем неделю, можете поставить меньше если хотите проверить
        await asyncio.sleep(7*24*60*60)



if __name__ == '__main__':
    # Запускаем задачи
    loop = asyncio.get_event_loop()
    loop.create_task(remind_about_exercises())
    loop.create_task(remind_about_goal())

    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)