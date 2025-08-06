# python bot.py
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CHANNEL_USERNAME = "+H_Gem2w733JlOWYy"  
PAYMENT_LINK = "https://send.monobank.ua/jar/8213RMymLZ"

# Google Sheets setup

# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(credentials)
# sheet = client.open("UKbot").sheet1

import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Скоупи для доступу до Google Sheets та Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Отримуємо JSON зі змінної середовища
creds_json = os.getenv("GOOGLE_CREDS_JSON")
if creds_json is None:
    raise ValueError("GOOGLE_CREDS_JSON змінна не встановлена!")

# Завантажуємо JSON як словник
creds_dict = json.loads(creds_json)

# Створюємо credentials з dict
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Авторизуємось через gspread
client = gspread.authorize(credentials)

# Відкриваємо таблицю
sheet = client.open("UKbot").sheet1

# FSM для збору даних
class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    proof = State()

# Ініціалізація бота та диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
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
        "🇺🇦 Привіт! Це бот У-Кварталу, за допомогою якого ми збираємо 200 000 грн на ремонт лікарняних палат у військовому госпіталі 🏥✨\n\n"
        "💛 За твій донат від 500 грн ти автоматично отримуєш сертифікат 🎟️ на повний день в U-Wellness Space 🧖‍♂️🌿\n\n"
        "Для початку введи своє ім’я: 📝😊"
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
    await message.answer("Введіть номер телефону:")
    await state.set_state(Form.phone)

# Отримання телефону і надсилання посилання на оплату
@dp.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(
        f"💳 <b>Дякуємо за готовність підтримати!</b>\n\n"
        f"Ось посилання для оплати збору:\n👉 <a href='{PAYMENT_LINK}'>Оплатити тут</a>\n\n"
        "✅ Після оплати, будь ласка, <b>надішли скріншот</b> з підтвердженням переказу 🙏"
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
        f"{name}, дякуємо за участь у благодійному зборі!\n\n"
        f"💙💛 Твоя підтримка — це крок до перемоги й турботи про наших захисників!\n\n"
        f"🎫 Ваш номер сертифікату:🎉<b>{cert_number}</b>🎉\n\n"
        f"📍  Отримати сертифікат можна у U-Wellness Space з 29 серпня\n"
        f"🗓️ Використати його можна впродовж вересня у будь-який день!\n\n"
    )
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
