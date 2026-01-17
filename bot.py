from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import openai

# --- Настройки ---
API_TOKEN = "8304477592:AAE648DGz_BHGAhMkaNzbIzWci6molN8zYI"
OPENAI_API_KEY = "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"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# --- Кнопки ---
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Generation"))
keyboard.add(KeyboardButton("Speaks Truth"))
keyboard.add(KeyboardButton("Normal AI"))

# --- Хранение режима пользователей ---
user_modes = {}

# --- Старт ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Welcome to TruthBot! Choose a mode:", reply_markup=keyboard)

# --- Обработка сообщений ---
@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Выбор режима
    if text.lower() == "generation":
        user_modes[user_id] = "gen"
        await message.answer("Generation in development 🖼")
        return
    elif text.lower() == "speaks truth":
        user_modes[user_id] = "truth"
        await message.answer("Truth mode activated 😈")
        return
    elif text.lower() == "normal ai":
        user_modes[user_id] = "normal"
        await message.answer("Normal AI mode activated 🙂")
        return

    mode = user_modes.get(user_id, "normal")

    # --- Формируем промпт ---
    if mode == "truth":
        prompt = f"""
Ты — дерзкий, токсичный ИИ с чётким юмором и матом. 
Отвечай коротко, прямолинейно, почти всегда используй мат, сарказм, и жесткие шутки. 
Не используй эмодзи. 
Пользователь написал: "{text}"
Ответь как токсикально и смешно, но максимально жёстко.
"""
    elif mode == "normal":
        prompt = f"""
Ты — умный, спокойный и поддерживающий ИИ. 
Отвечай коротко и по делу. 
Пользователь написал: "{text}"
"""
    elif mode == "gen":
        await message.answer("Generation in development 🖼")
        return

    # --- Запрос к OpenAI ---
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150,
            temperature=0.9
        )
        answer = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        answer = f"Ошибка ИИ: {str(e)}"

    await message.answer(answer)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
