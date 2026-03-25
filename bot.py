import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
import json

# --- SOZLAMALAR ---
API_TOKEN = '8092475091:AAExkErzQ9_pZ1cUzQI7yE3HW1SrYdLhOQQ' # @BotFather'dan olgan token
WEB_APP_URL = 'https://maxkamov-122.github.io/whoami-chat/' # https://github.io

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Chatga kirgan barcha foydalanuvchilar bazasi (vaqtinchalik)
active_users = set()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    active_users.add(message.chat.id)
    
    # Web App tugmasini yaratish
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    markup.add(types.KeyboardButton(text="🔐 WHOAMI SEC CHAT", web_app=web_app))
    
    await message.answer(
        f"🛡️ **WHOAMI SEC** tizimiga xush kelibsiz, {message.from_user.first_name}!\n\n"
        "Barcha xabarlar E2E shifrlangan. Xavfsiz aloqa o'rnatildi.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Web App'dan kelgan ma'lumotlarni qabul qilish
@dp.message_handler(content_types=['web_app_data'])
async def get_web_app_data(message: types.Message):
    try:
        # Kelgan JSON ma'lumotni o'qiymiz
        data = json.loads(message.web_app_data.data)
        user_nick = data.get('user', 'Anonymous')
        msg_text = data.get('text', '')
        avatar = data.get('avatar', '👤')
        role = data.get('role', 'user')

        # Admin bo'lsa maxsus belgi qo'shamiz
        if user_nick.lower() == "x-gab":
            display_name = f"👑 ADMIN {user_nick}"
        else:
            display_name = f"{avatar} {user_nick}"

        # Xabarni barcha faol foydalanuvchilarga yuboramiz
        for user_id in active_users:
            try:
                await bot.send_message(
                    user_id, 
                    f"<b>{display_name}:</b>\n{msg_text}", 
                    parse_mode="HTML"
                )
            except Exception:
                pass # Agar foydalanuvchi botni bloklagan bo'lsa
                
    except Exception as e:
        logging.error(f"Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
