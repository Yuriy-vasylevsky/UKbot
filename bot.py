
# робоча версія 

# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import Message, FSInputFile
# from aiogram.enums import ParseMode
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.default import DefaultBotProperties

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import uuid
# import os

# # Бот
# BOT_TOKEN = "8371853976:AAGxedICmLKYvjxSeQqBiZn_N95Hv0hrA1I"
# bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# dp = Dispatcher(storage=MemoryStorage())

# # Google Sheets підключення
# gc = gspread.service_account(filename="credentials.json")
# spreadsheet = gc.open("UKbot")
# worksheet = spreadsheet.sheet1

# # Стан
# class Form(StatesGroup):
#     name = State()
#     surname = State()
#     phone = State()
#     proof = State()

# # Старт
# @dp.message(F.text == "/start")
# async def start(message: Message, state: FSMContext):
#     await message.answer(
#         "Привіт! Це бот для участі у <b>благодійному зборі</b> 🎟️\n\n"
#         "Зараз я зафіксую твої дані, а потім ти отримаєш посилання на оплату."
#     )
#     await message.answer("Введи, будь ласка, <b>своє імʼя</b>:")
#     await state.set_state(Form.name)

# @dp.message(Form.name)
# async def process_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Тепер введи <b>прізвище</b>:")
#     await state.set_state(Form.surname)

# @dp.message(Form.surname)
# async def process_surname(message: Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await message.answer("Введи <b>номер телефону</b>:")
#     await state.set_state(Form.phone)

# @dp.message(Form.phone)
# async def process_phone(message: Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer("🔗 <b>Посилання на оплату:</b>\nhttps://send.monobank.ua/jar/XXXXXXXXXX\n\nПісля оплати пришли скріншот.")
#     await state.set_state(Form.proof)

# @dp.message(Form.proof, F.photo)
# async def process_proof(message: Message, state: FSMContext):
#     data = await state.get_data()
#     participant_id = str(uuid.uuid4())[:4].upper()

#     # Зберегти в Google Таблицю
#     worksheet.append_row([
#         participant_id,
#         data['name'],
#         data['surname'],
#         data['phone']
#     ])

#     # Отримати останнє фото (найбільша якість)
#     photo = message.photo[-1]
#     file = await bot.get_file(photo.file_id)

#     # Завантажити файл локально
#     os.makedirs("screenshots", exist_ok=True)
#     destination_path = f"screenshots/{participant_id}.jpg"
#     file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

#     # Скачати через aiohttp (оскільки bot.download може іноді давати помилки)
#     import aiohttp
#     async with aiohttp.ClientSession() as session:
#         async with session.get(file_url) as resp:
#             if resp.status == 200:
#                 with open(destination_path, "wb") as f:
#                     f.write(await resp.read())

#     await message.answer(
#         f"✅ Дякуємо за участь у зборі!\n"
#         f"Твій номер: <b>{participant_id}</b>.\n"
#         f"Дані збережено 💙"
#     )

#     await state.clear()
# # Запуск
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(dp.start_polling(bot))


# python bot.py

# зберігає скріни в тг

# import asyncio
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.enums import ParseMode

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# BOT_TOKEN = "8371853976:AAGxedICmLKYvjxSeQqBiZn_N95Hv0hrA1I"
# CHANNEL_ID = -1002575438586  # заміни на ID твого каналу

# # Google Sheets setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(credentials)
# sheet = client.open("UKbot").sheet1

# # FSM для збору даних
# class Form(StatesGroup):
#     name = State()
#     surname = State()
#     phone = State()
#     proof = State()

# # Ініціалізація
# bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
# dp = Dispatcher(storage=MemoryStorage())

# # Команда /start
# @dp.message(F.text == "/start")
# async def start(message: Message, state: FSMContext):
#     await message.answer(
#         "Привіт! Це бот для збору на благодійність.\n\n"
#         "Будь ласка, введи своє ім’я:"
#     )
#     await state.set_state(Form.name)

# # Ім’я
# @dp.message(Form.name)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Тепер введи прізвище:")
#     await state.set_state(Form.surname)

# # Прізвище
# @dp.message(Form.surname)
# async def get_surname(message: Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await message.answer("Введи номер телефону:")
#     await state.set_state(Form.phone)

# # Телефон
# @dp.message(Form.phone)
# async def get_phone(message: Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer("Тепер надішли скріншот з оплатою:")
#     await state.set_state(Form.proof)

# # Скриншот
# @dp.message(Form.proof, F.photo)
# async def process_proof(message: Message, state: FSMContext):
#     data = await state.get_data()
#     name = data['name']
#     surname = data['surname']
#     phone = data['phone']

#     photo = message.photo[-1]  # найвища якість
#     file_id = photo.file_id

#     # Надсилаємо фото в канал
#     await bot.send_photo(
#         chat_id=CHANNEL_ID,
#         photo=file_id,
#         caption=f"✅ Оплата від: <b>{name} {surname}</b>\n📞 {phone}"
#     )

#     # Зберігаємо в таблицю
#     sheet.append_row([name, surname, phone])

#     await message.answer("Дякуємо за участь у зборі! 💙💛")
#     await state.clear()

# # Запуск
# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())


# python bot.py

# Майже все робить лише посилання погане

# import asyncio
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.enums import ParseMode

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# BOT_TOKEN = "8371853976:AAGxedICmLKYvjxSeQqBiZn_N95Hv0hrA1I"
# CHANNEL_ID = -1002575438586  # заміни на ID твого каналу

# # Посилання на оплату (банк збору)
# PAYMENT_LINK = "https://your-payment-link.example.com"

# # Google Sheets setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(credentials)
# sheet = client.open("UKbot").sheet1

# # FSM для збору даних
# class Form(StatesGroup):
#     name = State()
#     surname = State()
#     phone = State()
#     proof = State()

# # Ініціалізація бота та диспетчера
# bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
# dp = Dispatcher(storage=MemoryStorage())

# # Функція для генерації номера сертифікату (наприклад, 3-значний номер за кількістю записів +1)
# def generate_certificate_number():
#     try:
#         records = sheet.get_all_records()
#         next_number = len(records) + 1
#         return f"{next_number:03d}"  # наприклад, 001, 002, 003 ...
#     except Exception:
#         return "001"

# # Команда /start
# @dp.message(F.text == "/start")
# async def start(message: Message, state: FSMContext):
#     await message.answer(
#         "Привіт! Це бот для збору на благодійність.\n\n"
#         "Ми збираємо кошти для важливої справи, будь ласка, допоможи нам.\n\n"
#         "Для початку введи своє ім’я:"
#     )
#     await state.set_state(Form.name)

# # Отримання імені
# @dp.message(Form.name)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Тепер введи прізвище:")
#     await state.set_state(Form.surname)

# # Отримання прізвища
# @dp.message(Form.surname)
# async def get_surname(message: Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await message.answer("Введи номер телефону (у форматі +380XXXXXXXXX):")
#     await state.set_state(Form.phone)

# # Отримання телефону і надсилання посилання на оплату
# @dp.message(Form.phone)
# async def get_phone(message: Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer(
#         f"Дякую! Ось посилання для оплати збору:\n\n"
#         f"<a href='{PAYMENT_LINK}'>Оплатити тут</a>\n\n"
#         "Після оплати надішли, будь ласка, скріншот підтвердження оплати."
#     )
#     await state.set_state(Form.proof)

# # Обробка скріншоту з оплатою
# @dp.message(Form.proof, F.photo)
# async def process_proof(message: Message, state: FSMContext):
#     data = await state.get_data()
#     name = data['name']
#     surname = data['surname']
#     phone = data['phone']
#     photo = message.photo[-1]  # найвища якість
#     file_id = photo.file_id

#     # Генеруємо номер сертифікату
#     cert_number = generate_certificate_number()

#     # Надсилаємо фото в канал з інформацією
#     await bot.send_photo(
#         chat_id=CHANNEL_ID,
#         photo=file_id,
#         caption=(
#             f"✅ Оплата від: <b>{name} {surname}</b>\n"
#             f"📞 Телефон: {phone}\n"
#             f"🔗 Посилання на оплату: {PAYMENT_LINK}\n"
#             f"🎫 Номер сертифікату: {cert_number}"
#         )
#     )

#     # Зберігаємо в таблицю: ім'я, прізвище, телефон, посилання на оплату, номер сертифікату
#     sheet.append_row([name, surname, phone, PAYMENT_LINK, cert_number])

#     # Відповідь користувачу
#     await message.answer(
#         f"Дякуємо за участь у благодійному зборі! 💙💛\n"
#         f"Ваш номер сертифікату: <b>{cert_number}</b>"
#     )
#     await state.clear()

# # Запуск бота
# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN = "8371853976:AAGxedICmLKYvjxSeQqBiZn_N95Hv0hrA1I"
CHANNEL_ID = -1002575438586  # ID твого каналу (числовий)
CHANNEL_USERNAME = "ukzbir"  # без @ — коротке ім'я твого каналу

# Посилання на оплату (банк збору)
PAYMENT_LINK = "https://your-payment-link.example.com"

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("UKbot").sheet1

# FSM для збору даних
class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    proof = State()

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Функція для генерації номера сертифікату (3-значний номер за кількістю записів +1)
def generate_certificate_number():
    try:
        next_number = len(sheet.get_all_values())
        return f"{next_number:03d}"  # 001, 002, 003 ...
    except Exception:
        return "001"

# Команда /start
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Привіт! Це бот для збору на благодійність.\n\n"
        "Ми збираємо кошти для важливої справи, будь ласка, допоможи нам.\n\n"
        "Для початку введи своє ім’я:"
    )
    await state.set_state(Form.name)

# Отримання імені
@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Тепер введи прізвище:")
    await state.set_state(Form.surname)

# Отримання прізвища
@dp.message(Form.surname)
async def get_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введи номер телефону (у форматі +380XXXXXXXXX):")
    await state.set_state(Form.phone)

# Отримання телефону і надсилання посилання на оплату
@dp.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(
        f"Дякую! Ось посилання для оплати збору:\n\n"
        f"<a href='{PAYMENT_LINK}'>Оплатити тут</a>\n\n"
        "Після оплати надішли, будь ласка, скріншот підтвердження оплати."
    )
    await state.set_state(Form.proof)

# Обробка скріншоту з оплатою
@dp.message(Form.proof, F.photo)
async def process_proof(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    surname = data['surname']
    phone = data['phone']
    photo = message.photo[-1]  # найвища якість
    file_id = photo.file_id

    # Генеруємо номер сертифікату
    cert_number = generate_certificate_number()

    # Відправляємо фото в канал і отримуємо об'єкт повідомлення
    sent_msg = await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=file_id,
        caption=(
            f"✅ Оплата від: <b>{name} {surname}</b>\n"
            f"📞 Телефон: {phone}\n"
            f"🔗 Посилання на оплату: {PAYMENT_LINK}\n"
            f"🎫 Номер сертифікату: {cert_number}"
        )
    )

    # Формуємо посилання на повідомлення в каналі
    message_link = f"https://t.me/{CHANNEL_USERNAME}/{sent_msg.message_id}"

    # Зберігаємо в таблицю: ім'я, прізвище, телефон, посилання на повідомлення в каналі, номер сертифікату
    sheet.append_row([name, surname, phone, message_link, cert_number])

    # Відповідаємо користувачу з номером сертифікату і посиланням
    await message.answer(
        f"Дякуємо за участь у благодійному зборі! 💙💛\n"
        f"Ваш номер сертифікату: <b>{cert_number}</b>\n"
        
    )
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
