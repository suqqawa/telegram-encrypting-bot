import asyncio
import base64
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cryptography.fernet import Fernet
from caesar_cipher import encrypt_caesar, decrypt_caesar
from vigenere_cipher import encrypt_vigenere, decrypt_vigenere

TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher()

fernet_key = Fernet.generate_key()
fernet = Fernet(fernet_key)

user_states = {}
encrypted_messages = {}

def get_encryption_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Base64 шифрование", callback_data="encrypt_base64")],
        [InlineKeyboardButton(text="Шифр Цезаря", callback_data="encrypt_caesar")],
        [InlineKeyboardButton(text="Шифр Виженера", callback_data="encrypt_vigenere")],
        [InlineKeyboardButton(text="Бинарное преобразование", callback_data="encrypt_binary")],
        [InlineKeyboardButton(text="Fernet шифрование", callback_data="encrypt_fernet")]
    ])
    return keyboard

def get_decryption_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Base64 расшифровка", callback_data="decrypt_base64")],
        [InlineKeyboardButton(text="Расшифровка шифра Цезаря", callback_data="decrypt_caesar")],
        [InlineKeyboardButton(text="Расшифровка шифра Виженера", callback_data="decrypt_vigenere")],
        [InlineKeyboardButton(text="Бинарная расшифровка", callback_data="decrypt_binary")],
        [InlineKeyboardButton(text="Fernet расшифровка", callback_data="decrypt_fernet")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в бот шифрования!\n\n"
        "Используйте следующие команды:\n"
        "📝 /encrypt - зашифровать сообщение\n"
        "🔓 /decrypt - расшифровать сообщение"
    )

@dp.message(Command("info"))
async def cmd_start(message: types.Message):
    await message.answer(
        """Хочешь узнать подробнее о методах шифрования?Сейчас расскажу.
        =======================================================================================================================
        1)Base64– способ кодирования произвольных двоичных данных в ASCII текст.
        По своей сути кодирование очень простое. Каждые шесть бит на входе кодируется в один из символов 64-буквенного алфавита.
        “Стандартный” алфавит, который для этого используется – это. A-Z, a-z, 0-9, +, / и= в качестве заполняющего символа в конце.
        Таким образом, на каждые 3 байта данных приходится 4 символа.
        =======================================================================================================================
        2)Шифр Цезаря — это один из самых простых и старейших методов шифрования. 
        Он был назван в честь римского императора Юлия Цезаря, который использовал его для секретной переписки.
        Принцип работы шифра заключается в том, что каждая буква в тексте сдвигается на фиксированное количество позиций по алфавиту. 
        Например, если сдвиг равен 3, то буква «А» становится «Г», «Б» — «Д» и так далее.
        =======================================================================================================================
        3)Шифр Виженера — метод полиалфавитного шифрования буквенного текста с использованием ключевого слова. 
        Метод прост для понимания и реализации, он является недоступным для простых методов криптоанализа. 
        Хотя шифр легко понять и реализовать, на протяжении трех столетий он противостоял всем попыткам его сломать. 
        Шифр Виженера размывает характеристики частот появления символов в тексте, но некоторые особенности появления символов в тексте остаются.
        =======================================================================================================================
        4)Шифр Вернама (XOR-шифр) — метод шифрования на основе бинарного преобразования. Это простейший шифр на основе бинарной логики, который обладает абсолютной криптографической стойкостью.
        Процесс шифрования:
        Сообщение разбивают на отдельные символы и каждый символ представляют в бинарном виде. 
        Вводят текст для шифровки и ключ такой же длины. 
        Переводят каждую букву в её бинарный код и выполняют формулу сообщение XOR ключ. 
        =======================================================================================================================
        5)Fernet — это метод шифрования, который обеспечивает симметричное шифрование и аутентификацию данных. Он является частью криптографической библиотеки для Python. 
        Принцип работы: при шифровании сообщения с помощью Fernet на входе передаются открытый текст, ключ и временная метка, а затем на основе этой информации создаётся токен. 
        Токен включает в себя зашифрованную версию открытого текста, а также информацию, необходимую для проверки целостности сообщения. Это предотвращает чтение или изменение сообщения без ключа. 
        """
    )

@dp.message(Command("encrypt"))
async def cmd_encrypt(message: types.Message):
    user_states[message.from_user.id] = "waiting_for_encrypt_text"
    await message.answer("Введите текст, который хотите зашифровать:")

@dp.message(Command("decrypt"))
async def cmd_decrypt(message: types.Message):
    user_states[message.from_user.id] = "waiting_for_decrypt_text"
    await message.answer("Введите текст, который хотите расшифровать:")

@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return

    state = user_states[user_id]
    if state == "waiting_for_encrypt_text":
        encrypted_messages[user_id] = message.text
        await message.answer("Выберите метод шифрования:", reply_markup=get_encryption_keyboard())
    elif state == "waiting_for_decrypt_text":
        encrypted_messages[user_id] = message.text
        await message.answer("Выберите метод расшифровки:", reply_markup=get_decryption_keyboard())

@dp.callback_query()
async def handle_encryption_choice(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    text = encrypted_messages.get(user_id, "")
    method = callback.data

    result = ""
    if method == "encrypt_base64":
        result = base64.b64encode(text.encode()).decode()
    elif method == "decrypt_base64":
        try:
            result = base64.b64decode(text.encode()).decode()
        except:
            result = "❌ Неверный формат Base64"

    elif method == "encrypt_caesar":
        result = encrypt_caesar(text)
    elif method == "decrypt_caesar":
        result = decrypt_caesar(text)

    elif method == "encrypt_vigenere":
        result = encrypt_vigenere(text, "КЛЮЧ")
    elif method == "decrypt_vigenere":
        result = decrypt_vigenere(text, "КЛЮЧ")

    elif method == "encrypt_binary":
        result = ' '.join(format(ord(c), '08b') for c in text)
    elif method == "decrypt_binary":
        try:
            result = ''.join(chr(int(b, 2)) for b in text.split())
        except:
            result = "❌ Неверный бинарный формат"

    elif method == "encrypt_fernet":
        result = fernet.encrypt(text.encode()).decode()
    elif method == "decrypt_fernet":
        try:
            result = fernet.decrypt(text.encode()).decode()
        except:
            result = "❌ Неверный формат Fernet шифрования"

    await callback.message.answer(
        f"✅ Результат:\n"
        f"{'='*30}\n"
        f"{result}\n"
        f"{'='*30}"
    )
    await callback.answer()

    if user_id in user_states:
        del user_states[user_id]
    if user_id in encrypted_messages:
        del encrypted_messages[user_id]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
