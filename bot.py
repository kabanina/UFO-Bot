import os
import random
import threading
import time
import telebot
from flask import Flask
from telebot import types
from leksik import VOCAB  # Імпортуємо словник із твого файлу leksik.py

TOKEN = os.getenv("BOT_TOKEN", "8693317472:AAGj4wgSYLRtSn7w8_Wniteu1MQEbJCXy08")
bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=["start", "next"])
def send_word(message):
    chat_id = message.chat.id
    item = random.choice(VOCAB)
    user_data[chat_id] = item

    markup = types.InlineKeyboardMarkup()
    btn_show = types.InlineKeyboardButton(
        "👁 Німецький переклад / Приклад", callback_data="show"
    )
    btn_next = types.InlineKeyboardButton("➡️ Наступне слово", callback_data="next")
    markup.add(btn_show, btn_next)

    bot.send_message(
        chat_id,
        f"🇺🇦 Слово: **{item['translation']}**\n\nЯк це буде німецькою?",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    item = user_data.get(chat_id)

    if call.data == "show" and item:
        bot.answer_callback_query(call.id)
        text = f"🇺🇦 Слово: **{item['translation']}**\n🇩🇪 Німецькою: **{item['word']}**\n\n💡 Приклад: _{item['example']}_"

        markup = types.InlineKeyboardMarkup()
        btn_next = types.InlineKeyboardButton(
            "➡️ Наступне слово", callback_data="next"
        )
        markup.add(btn_next)

        bot.edit_message_text(
            text,
            chat_id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup,
        )

    elif call.data == "next":
        bot.answer_callback_query(call.id)
        send_word(call.message)


# --- Вебсервер для Render (тримає порт відкритим) ---
app = Flask(__name__)


@app.route("/")
def home():
    return "Goethe A1 Vocabulary Trainer is running!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# Запуск Flask у фоновому потоці
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Запуск бота з примусовим видаленням вебхука та авторестартом
if __name__ == "__main__":
    print("Бот і вебсервер успішно запущені!")
    try:
        bot.remove_webhook()  # Скидаємо старий вебхук, щоб полінг запрацював
    except Exception as e:
        print(f"Помилка при видаленні вебхука: {e}")

    while True:
        try:
            bot.infinity_polling(none_stop=True, interval=1, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Помилка в полінгу, перезапуск через 5 сек: {e}")
            time.sleep(5)
