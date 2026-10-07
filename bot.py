import random
import telebot
from telebot import types

TOKEN = "8693317472:AAGj4wgSYLRtSn7w8_Wniteu1MQEbJCXy08"
bot = telebot.TeleBot(TOKEN)

# База слів із документа Goethe A1
VOCAB = [
    {"word": "abfahren", "translation": "відправлятися", "example": "Wir fahren um zwölf Uhr ab."},
    {"word": "die Abfahrt", "translation": "відправлення", "example": "Vor der Abfahrt rufe ich an."},
    {"word": "abgeben", "translation": "здавати, віддавати", "example": "Ich muss meine Schlüssel abgeben."},
    {"word": "abholen", "translation": "забирати", "example": "Wann kann ich den Schrank bei dir abholen?"},
    {"word": "die Adresse, -n", "translation": "адреса", "example": "Können Sie mir seine Adresse sagen?"},
    {"word": "allein", "translation": "сам, самостійно", "example": "Er kommt allein."},
    {"word": "alt", "translation": "старий", "example": "Mein Auto ist schon sehr alt."},
    {"word": "das Alter", "translation": "вік", "example": "Alter: 26 Jahre."},
    {"word": "anfangen", "translation": "починатися", "example": "Der Unterricht fängt gleich an."},
    {"word": "ankommen", "translation": "прибувати", "example": "Wann kommt dieser Zug in Hamburg an?"},
    {"word": "anmachen", "translation": "вмикати", "example": "Mach bitte das Licht an!"},
    {"word": "sich anmelden", "translation": "реєструватися, записуватися", "example": "Wo kann ich mich anmelden?"},
    {"word": "anrufen", "translation": "телефонувати", "example": "Peter ruft kurz seine Freundin an."},
    {"word": "antworten", "translation": "відповідати", "example": "Er antwortet nicht."},
    {"word": "sich anziehen", "translation": "одягатися", "example": "Ich muss mich noch anziehen."},
    {"word": "der Apfel, -ä", "translation": "яблуко", "example": "Ein Pfund Äpfel bitte."},
    {"word": "arbeiten", "translation": "працювати", "example": "Wo arbeiten Sie?"},
    {"word": "aufhören", "translation": "припинятися, закінчуватися", "example": "Der Kurs hört in einer Woche auf."},
    {"word": "aufstehen", "translation": "вставати", "example": "Ich muss immer um vier Uhr aufstehen."},
    {"word": "ausfüllen", "translation": "заповнювати", "example": "Füllen Sie bitte dieses Formular aus."},
    {"word": "aussteigen", "translation": "виходити (з транспорту)", "example": "Wo muss ich aussteigen?"},
    {"word": "bedeuten", "translation": "означати", "example": "Was bedeutet das Wort?"},
    {"word": "beginnen", "translation": "починатися", "example": "Das Spiel beginnt um 15.30 Uhr."},
    {"word": "bestellen", "translation": "замовляти", "example": "Wir möchten bestellen, bitte."},
    {"word": "besuchen", "translation": "відвідувати", "example": "Darf ich dich besuchen?"},
    {"word": "bezahlen", "translation": "оплачувати", "example": "Wo muss ich bezahlen?"},
    {"word": "bleiben", "translation": "залишатися", "example": "Ich bleibe heute zu Hause."},
    {"word": "brauchen", "translation": "потребувати", "example": "Brauchst du die Zeitung noch?"},
    {"word": "bringen", "translation": "приносити", "example": "Bringen Sie mir bitte noch einen Kaffee!"},
    {"word": "einkaufen", "translation": "робити покупки", "example": "Ich muss noch einkaufen."},
    {"word": "einladen", "translation": "запрошувати", "example": "Darf ich dich einladen?"},
    {"word": "empfehlen", "translation": "рекомендувати", "example": "Was können Sie empfehlen?"},
    {"word": "fehlen", "translation": "бракувати, боліти", "example": "Was fehlt Ihnen?"},
    {"word": "fernsehen", "translation": "дивитися телевізор", "example": "Wollen wir fernsehen?"},
    {"word": "gefallen", "translation": "подобатися", "example": "Das gefällt mir."},
    {"word": "gehören", "translation": "належати", "example": "Wem gehört das Auto?"},
    {"word": "kennenlernen", "translation": "знайомитися", "example": "Wir möchten Sie kennenlernen."},
    {"word": "reparieren", "translation": "ремонтувати", "example": "Er hat das Auto repariert."},
    {"word": "umziehen", "translation": "переїжджати", "example": "Nächsten Monat ziehen wir um."},
    {"word": "verstehen", "translation": "розуміти", "example": "Können Sie mich verstehen?"}
]

user_data = {}

@bot.message_handler(commands=['start', 'next'])
def send_word(message):
    chat_id = message.chat.id
    item = random.choice(VOCAB)
    user_data[chat_id] = item

    markup = types.InlineKeyboardMarkup()
    btn_show = types.InlineKeyboardButton("👁 Німецький переклад / Приклад", callback_data="show")
    btn_next = types.InlineKeyboardButton("➡️ Наступне слово", callback_data="next")
    markup.add(btn_show, btn_next)

    bot.send_message(
        chat_id, 
        f"🇺🇦 Слово: **{item['translation']}**\n\nЯк це буде німецькою?", 
        parse_mode="Markdown", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    item = user_data.get(chat_id)

    if call.data == "show" and item:
        bot.answer_callback_query(call.id)
        text = f"🇺🇦 Слово: **{item['translation']}**\n🇩🇪 Німецькою: **{item['word']}**\n\n💡 Приклад: _{item['example']}_"
        
        markup = types.InlineKeyboardMarkup()
        btn_next = types.InlineKeyboardButton("➡️ Наступне слово", callback_data="next")
        markup.add(btn_next)
        
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "next":
        bot.answer_callback_query(call.id)
        send_word(call.message)

bot.polling(none_stop=True)