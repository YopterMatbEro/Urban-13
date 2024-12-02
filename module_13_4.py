from aiogram import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from data import dp


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Введите слово "Calories" для подсчета нормы калорий для поддержания нормального веса.')


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст.')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    if message.text.isdigit() and 0 < int(message.text) < 120:
        await state.update_data(age=message.text)
        await message.answer('Введите свой рост в сантиметрах.')
        await UserState.growth.set()
    else:
        await message.answer('Пожалуйста, введите корректный возраст (число в диапазоне от 1 до 120 лет). Попробуйте снова.')


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    if message.text.isdigit() and 30 < int(message.text) < 300:
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес в килограммах.')
        await UserState.weight.set()
    else:
        await message.answer('Пожалуйста, введите корректный рост (число в диапазоне от 30 до 300 см). Попробуйте снова.')


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    if message.text.isdigit() and 10 < int(message.text) < 400:
        await state.update_data(weight=message.text)
        await message.answer('Укажите свой пол (М/Ж)')
        await UserState.gender.set()
    else:
        await message.answer('Пожалуйста, введите корректный вес (число в диапазоне от 10 до 400 кг). Попробуйте снова.')


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    gender = message.text.lower()
    if gender in ['м', 'ж']:
        await state.update_data(gender=message.text)
        data = await state.get_data()
        if data['gender'].lower() == 'м':
            result = (10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5) * 1.55  # выбрал среднюю активность
            await message.answer(f'Норма калорий для Вас {round(result, 2)}')
        elif data['gender'].lower() == 'ж':
            result = (10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161) * 1.55
            await message.answer(f'Норма калорий для Вас {round(result, 2)}')
    else:
        await message.answer(f'Неверно указан пол, Ваш ответ: {gender}')
        await message.answer('Начните сначала. Введите команду /start')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение!')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
