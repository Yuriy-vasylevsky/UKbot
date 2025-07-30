
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
