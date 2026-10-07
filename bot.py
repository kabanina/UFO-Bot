import os
import random
import threading
import telebot
from flask import Flask
from telebot import types

TOKEN = os.getenv("BOT_TOKEN", "8693317472:AAGj4wgSYLRtSn7w8_Wniteu1MQEbJCXy08")
bot = telebot.TeleBot(TOKEN)

# Повний словник Goethe-Zertifikat A1 з офіційного документа
VOCAB = [
    {
        "word": "ab",
        "translation": "від, з",
        "example": "Ab morgen muss ich arbeiten.",
    },
    {
        "word": "aber",
        "translation": "але",
        "example": "Ich bin oft im Büro, aber nur für wenige Stunden.",
    },
    {
        "word": "abfahren",
        "translation": "відправлятися",
        "example": "Wir fahren um zwölf Uhr ab.",
    },
    {
        "word": "die Abfahrt",
        "translation": "відправлення",
        "example": "Vor der Abfahrt rufe ich an.",
    },
    {
        "word": "abgeben",
        "translation": "здавати, віддавати",
        "example": "Ich muss meine Schlüssel abgeben.",
    },
    {
        "word": "abholen",
        "translation": "забирати",
        "example": "Wann kann ich den Schrank bei dir abholen?",
    },
    {
        "word": "die Adresse, -n",
        "translation": "адреса",
        "example": "Können Sie mir seine Adresse sagen?",
    },
    {
        "word": "all- (alles, alle)",
        "translation": "весь, всі, все",
        "example": "Alles Gute! Sind alle da?",
    },
    {
        "word": "allein",
        "translation": "сам, самостійно",
        "example": "Er kommt allein.",
    },
    {
        "word": "also",
        "translation": "отже, і так",
        "example": "Also, es ist so...",
    },
    {
        "word": "alt",
        "translation": "старий",
        "example": "Wie alt sind Sie? Mein Auto ist schon sehr alt.",
    },
    {"word": "das Alter", "translation": "вік", "example": "Alter: 26 Jahre."},
    {
        "word": "an",
        "translation": "на, біля",
        "example": "Wir treffen uns am Bahnhof.",
    },
    {
        "word": "anbieten",
        "translation": "пропонувати",
        "example": "Was darf ich dir anbieten?",
    },
    {
        "word": "das Angebot, -e",
        "translation": "пропозиція, акція",
        "example": "Heute sind Sportschuhe im Angebot.",
    },
    {
        "word": "anfangen",
        "translation": "починатися",
        "example": "Der Unterricht fängt gleich an.",
    },
    {
        "word": "der Anfang",
        "translation": "початок",
        "example": "Wir wohnen am Anfang der Straße.",
    },
    {
        "word": "anklicken",
        "translation": "натиснути (клікнути) мишкою",
        "example": "Da musst du dieses Wort anklicken.",
    },
    {
        "word": "ankommen",
        "translation": "прибувати",
        "example": "Wann kommt dieser Zug in Hamburg an?",
    },
    {
        "word": "die Ankunft",
        "translation": "прибуття",
        "example": "Auf diesem Plan steht nur die Ankunft.",
    },
    {
        "word": "ankreuzen",
        "translation": "відзначити хрестиком",
        "example": "Auf dem Formular müssen Sie etwas ankreuzen.",
    },
    {
        "word": "anmachen",
        "translation": "вмикати",
        "example": "Mach bitte das Licht an!",
    },
    {
        "word": "sich anmelden",
        "translation": "реєструватися, записуватися",
        "example": "Wo kann ich mich anmelden?",
    },
    {
        "word": "die Anmeldung",
        "translation": "реєстрація",
        "example": "Eine Anmeldung ist nicht mehr möglich.",
    },
    {
        "word": "anrufen",
        "translation": "телефонувати",
        "example": "Peter ruft kurz seine Freundin an.",
    },
    {
        "word": "der Anruf, -e / Anrufbeantworter",
        "translation": "дзвінок / автовідповідач",
        "example": "Sprechen Sie auf den Anrufbeantworter.",
    },
    {
        "word": "antworten / die Antwort, -n",
        "translation": "відповідати / відповідь",
        "example": "Er antwortet nicht. Er gibt keine Antwort.",
    },
    {
        "word": "die Anzeige",
        "translation": "оголошення",
        "example": "Ich habe Ihre Anzeige in der Zeitung gelesen.",
    },
    {
        "word": "sich anziehen",
        "translation": "одягатися",
        "example": "Ich muss mich noch anziehen.",
    },
    {
        "word": "das Apartment, -s",
        "translation": "апартаменти",
        "example": "Wir haben ein Apartment gemietet.",
    },
    {
        "word": "der Apfel, -ä",
        "translation": "яблуко",
        "example": "Ein Pfund Äpfel bitte.",
    },
    {
        "word": "der Appetit",
        "translation": "апетит",
        "example": "Guten Appetit!",
    },
    {
        "word": "arbeiten / die Arbeit",
        "translation": "працювати / робота",
        "example": "Wo arbeiten Sie? Mein Bruder sucht Arbeit.",
    },
    {
        "word": "arbeitslos",
        "translation": "безробітний",
        "example": "Es gibt viele Leute, die arbeitslos sind.",
    },
    {
        "word": "der Arbeitsplatz, -ä, e",
        "translation": "робоче місце",
        "example": "An meinem Arbeitsplatz fehlt ein Drucker.",
    },
    {
        "word": "der Arm, -e",
        "translation": "рука (плече/передпліччя)",
        "example": "Mein Arm tut weh.",
    },
    {
        "word": "der Arzt, -ä, e",
        "translation": "лікар",
        "example": "Morgen habe ich einen Termin bei meiner Ärztin.",
    },
    {"word": "auch", "translation": "також", "example": "Ich bin auch Spanier."},
    {
        "word": "auf",
        "translation": "на",
        "example": "Die Kinder spielen auf der Straße.",
    },
    {
        "word": "die Aufgabe, -n",
        "translation": "завдання",
        "example": "Das ist eine schwere Aufgabe.",
    },
    {
        "word": "aufhören",
        "translation": "припинятися, закінчуватися",
        "example": "Der Kurs hört in einer Woche auf.",
    },
    {
        "word": "aufstehen",
        "translation": "вставати",
        "example": "Ich muss immer um vier Uhr aufstehen.",
    },
    {
        "word": "der Aufzug, -ü, e",
        "translation": "ліфт",
        "example": "In diesem Haus gibt es keinen Aufzug.",
    },
    {
        "word": "das Auge, -n",
        "translation": "око",
        "example": "Er hat blaue Augen.",
    },
    {
        "word": "aus",
        "translation": "з (звідкись)",
        "example": "Er kommt aus Brasilien.",
    },
    {
        "word": "der Ausflug, -ü, e",
        "translation": "екскурсія, поїздка",
        "example": "Morgen machen wir einen Ausflug.",
    },
    {
        "word": "ausfüllen",
        "translation": "заповнювати",
        "example": "Füllen Sie bitte dieses Formular aus.",
    },
    {
        "word": "der Ausgang, -ä, e",
        "translation": "вихід",
        "example": "Wo ist der Ausgang?",
    },
    {
        "word": "die Auskunft, -ü, e",
        "translation": "довідка, інформація",
        "example": "Können Sie mir eine Auskunft geben?",
    },
    {
        "word": "das Ausland / der Ausländer",
        "translation": "закордон / іноземець",
        "example": "Fahren Sie ins Ausland? Sind Sie Ausländer?",
    },
    {
        "word": "ausmachen",
        "translation": "вимикати",
        "example": "Mach bitte das Licht aus!",
    },
    {
        "word": "aussehen",
        "translation": "виглядати",
        "example": "Das sieht schön aus.",
    },
    {
        "word": "aussteigen",
        "translation": "виходити (з транспорту)",
        "example": "Wo muss ich aussteigen?",
    },
    {
        "word": "der Ausweis, -e",
        "translation": "посвідчення особи",
        "example": "Hier ist mein Ausweis.",
    },
    {
        "word": "das Baby, -s",
        "translation": "немовля",
        "example": "Mein Kind ist noch ein Baby.",
    },
    {
        "word": "die Bäckerei, -en",
        "translation": "пекарня",
        "example": "Ich geh mal schnell zur Bäckerei.",
    },
    {
        "word": "das Bad, -ä, er",
        "translation": "ванна кімната",
        "example": "Wir haben kein großes Bad.",
    },
    {
        "word": "baden",
        "translation": "купатися",
        "example": "Ich bade nicht so gern, ich dusche lieber.",
    },
    {
        "word": "die Bahn / der Bahnhof",
        "translation": "потяг / вокзал",
        "example": "Wir fahren mit der Bahn zum Bahnhof.",
    },
    {"word": "bald", "translation": "скоро", "example": "Ich komme bald."},
    {
        "word": "der Balkon, -s",
        "translation": "балкон",
        "example": "Die Wohnung hat einen kleinen Balkon.",
    },
    {
        "word": "die Bank, -en",
        "translation": "банк / лавка",
        "example": "Die Bank schließt um vier Uhr.",
    },
    {"word": "bar", "translation": "готівкою", "example": "Muss ich bar zahlen?"},
    {
        "word": "der Bauch, -ä, e",
        "translation": "живіт",
        "example": "Seit gestern tut mir the Bauch weh.",
    },
    {
        "word": "bedeuten",
        "translation": "означати",
        "example": "Was bedeutet das Wort?",
    },
    {
        "word": "beginnen",
        "translation": "починатися",
        "example": "Das Spiel beginnt um 15.30 Uhr.",
    },
    {
        "word": "bei",
        "translation": "у, при, біля",
        "example": "Ich wohne bei meinen Eltern.",
    },
    {"word": "beide", "translation": "обидва", "example": "Wir kommen beide."},
    {
        "word": "das Beispiel, -e",
        "translation": "приклад",
        "example": "Kannst du mir ein Beispiel sagen?",
    },
    {
        "word": "bekannt / der Bekannte",
        "translation": "відомий / знайомий",
        "example": "Ein Bekannter von mir heißt Klaus.",
    },
    {
        "word": "bekommen",
        "translation": "отримувати",
        "example": "Haben Sie meinen Brief bekommen?",
    },
    {
        "word": "benutzen",
        "translation": "користуватися",
        "example": "Die Aufzüge bitte nicht benutzen!",
    },
    {
        "word": "der Beruf, -e",
        "translation": "професія, фах",
        "example": "Was sind Sie von Beruf?",
    },
    {
        "word": "besetzt",
        "translation": "зайнятий",
        "example": "Die Nummer ist immer besetzt.",
    },
    {
        "word": "besichtigen",
        "translation": "оглядати",
        "example": "Ich möchte gern den Dom besichtigen.",
    },
    {
        "word": "besser / am besten",
        "translation": "краще / найкраще",
        "example": "Es geht mir schon besser.",
    },
    {
        "word": "bestellen",
        "translation": "замовляти",
        "example": "Wir möchten bestellen, bitte.",
    },
    {
        "word": "besuchen",
        "translation": "відвідувати",
        "example": "Darf ich dich besuchen?",
    },
    {
        "word": "das Bett, -en",
        "translation": "ліжко",
        "example": "Wir brauchen ein Kinderbett.",
    },
    {
        "word": "bezahlen",
        "translation": "оплачувати",
        "example": "Wo muss ich bezahlen?",
    },
    {
        "word": "das Bild, -er",
        "translation": "картина, фото",
        "example": "Hast du ein Bild von deinem Sohn?",
    },
    {
        "word": "billig",
        "translation": "дешевий",
        "example": "Die Jacke kostet nur 10 Euro! Die ist billig!",
    },
    {"word": "bis", "translation": "до", "example": "Ich warte bis morgen."},
    {
        "word": "bisschen",
        "translation": "трохи",
        "example": "Ich spreche ein bisschen Deutsch.",
    },
    {
        "word": "bitte / die Bitte",
        "translation": "будь ласка / прохання",
        "example": "Tasse Kaffee, bitte! Ich habe eine Bitte.",
    },
    {
        "word": "bitten",
        "translation": "просити",
        "example": "Darf ich Sie um etwas bitten?",
    },
    {
        "word": "bleiben",
        "translation": "залишатися",
        "example": "Ich bleibe heute zu Hause.",
    },
    {
        "word": "der Bleistift, -e",
        "translation": "олівець",
        "example": "Hast du einen Bleistift?",
    },
    {
        "word": "der Blick, -e",
        "translation": "вид, погляд",
        "example": "Man hat einen guten Blick auf den Rhein.",
    },
    {
        "word": "die Blume, -n",
        "translation": "квітка",
        "example": "Gefallen dir die Blumen?",
    },
    {
        "word": "böse",
        "translation": "злий, сердитий",
        "example": "Sie ist böse auf mich.",
    },
    {
        "word": "brauchen",
        "translation": "потребувати",
        "example": "Brauchst du die Zeitung noch?",
    },
    {
        "word": "breit",
        "translation": "широкий",
        "example": "Wie breit ist der Schrank?",
    },
    {
        "word": "der Brief, -e / die Briefmarke",
        "translation": "лист / поштова марка",
        "example": "Haben Sie einen Brief für mich?",
    },
    {
        "word": "bringen",
        "translation": "приносити",
        "example": "Bringen Sie mir bitte noch einen Kaffee!",
    },
    {
        "word": "das Brot, -e / das Brötchen",
        "translation": "хліб / булочка",
        "example": "Haben Sie Weißbrot und Brötchen?",
    },
    {
        "word": "der Bruder, -ü",
        "translation": "брат",
        "example": "Sein Bruder arbeitet auch hier.",
    },
    {
        "word": "das Buch, -ü, er",
        "translation": "книга",
        "example": "In diesem Wörterbuch finden Sie viele Wörter.",
    },
    {
        "word": "der Buchstabe / buchstabieren",
        "translation": "буква / вимовляти по літерах",
        "example": "Bitte buchstabieren Sie Ihren Namen.",
    },
    {
        "word": "der Bus, -se",
        "translation": "автобус",
        "example": "Wann kommt der nächste Bus?",
    },
    {
        "word": "das Café, -s / die CD",
        "translation": "кафе / компакт-диск",
        "example": "Sollen wir uns im Café treffen?",
    },
    {
        "word": "circa (ca.)",
        "translation": "приблизно",
        "example": "Es sind circa fünfzig Kilometer.",
    },
    {
        "word": "da",
        "translation": "там, ось",
        "example": "Da hinten ist er ja.",
    },
    {
        "word": "danke / danken",
        "translation": "дякувати / дякую",
        "example": "Ich danke Ihnen für die Einladung. Nein, danke!",
    },
    {
        "word": "dann",
        "translation": "потім, тоді",
        "example": "Ich muss zur Post, dann komme ich.",
    },
    {
        "word": "das",
        "translation": "це",
        "example": "Das ist sehr gut.",
    },
    {
        "word": "das Datum",
        "translation": "дата",
        "example": "Schreiben Sie das Datum auf das Formular.",
    },
    {
        "word": "dauern",
        "translation": "тривати",
        "example": "Wie lange dauert der Film?",
    },
    {
        "word": "denn",
        "translation": "оскільки, бо",
        "example": "Ich kann nicht kommen, denn ich bin krank.",
    },
    {
        "word": "deutsch",
        "translation": "німецький",
        "example": "Wie heißt das auf Deutsch?",
    },
    {
        "word": "drucken / der Drucker",
        "translation": "друкувати / принтер",
        "example": "Bitte drucke das für mich. Mein Drucker ist kaputt.",
    },
    {
        "word": "dürfen",
        "translation": "мати дозвіл",
        "example": "Sie dürfen hier nicht rauchen.",
    },
    {
        "word": "fahren / der Fahrer",
        "translation": "їхати / водій",
        "example": "Ich fahre mit dem Auto.",
    },
    {
        "word": "die Fahrkarte, -n",
        "translation": "квиток",
        "example": "Hast du schon eine Fahrkarte?",
    },
    {
        "word": "das Fahrrad, -ä, er",
        "translation": "велосипед",
        "example": "Fährst du mit dem Fahrrad?",
    },
    {
        "word": "falsch",
        "translation": "неправильно",
        "example": "Das ist falsch.",
    },
    {
        "word": "die Familie, -n / der Familienstand",
        "translation": "сім'я / сімейний стан",
        "example": "Meine Familie lebt in Spanien.",
    },
    {
        "word": "fehlen",
        "translation": "бракувати, боліти",
        "example": "Was fehlt Ihnen?",
    },
    {
        "word": "fernsehen",
        "translation": "дивитися телевізор",
        "example": "Wollen wir fernsehen?",
    },
    {
        "word": "finden",
        "translation": "знаходити",
        "example": "Wir müssen den Schlüssel finden.",
    },
    {
        "word": "fragen / die Frage, -n",
        "translation": "питати / запитання",
        "example": "Ich habe eine Frage.",
    },
    {
        "word": "frei",
        "translation": "віільний",
        "example": "Ist der Platz noch frei?",
    },
    {
        "word": "frühstücken / das Frühstück",
        "translation": "снідати / сніданок",
        "example": "Möchtest du ein Ei zum Frühstück?",
    },
    {
        "word": "geben",
        "translation": "давати",
        "example": "Kannst du mir deinen Kugelschreiber geben?",
    },
    {
        "word": "gefallen",
        "translation": "подобатися",
        "example": "Das gefällt mir.",
    },
    {
        "word": "gehen",
        "translation": "іти / йтися",
        "example": "Ich muss zum Arzt gehen. Wie geht's?",
    },
    {
        "word": "das Geld",
        "translation": "гроші",
        "example": "Hast du noch Geld?",
    },
    {
        "word": "gestern",
        "translation": "вчора",
        "example": "Gestern war ich krank.",
    },
    {
        "word": "glauben",
        "translation": "вірити, вважати",
        "example": "Ich glaube, er kommt gleich.",
    },
    {
        "word": "groß / klein",
        "translation": "великий / маленький",
        "example": "Frankfurt ist eine große Stadt.",
    },
    {
        "word": "gut / besser / am besten",
        "translation": "добре / краще / найкраще",
        "example": "Das finde ich gut.",
    },
    {
        "word": "haben",
        "translation": "мати",
        "example": "Ich habe ein neues Auto.",
    },
    {
        "word": "halten",
        "translation": "зупинятися",
        "example": "Dieser Zug hält in Mainz.",
    },
    {
        "word": "das Haus / nach Hause",
        "translation": "будинок / додому",
        "example": "Ich gehe jetzt nach Hause.",
    },
    {
        "word": "helfen / die Hilfe",
        "translation": "допомагати / допомога",
        "example": "Können Sie mir helfen? Hilfe!",
    },
    {
        "word": "kaufen / der Koffer",
        "translation": "купувати / валіза",
        "example": "Tim kauft einen Koffer.",
    },
    {
        "word": "kennenlernen",
        "translation": "знайомитися",
        "example": "Wir möchten Sie kennenlernen.",
    },
    {
        "word": "kochen / die Küche",
        "translation": "готувати / кухня",
        "example": "Herr Georgi kocht in der Küche.",
    },
    {
        "word": "kommen / woher",
        "translation": "приходити / звідки",
        "example": "Woher kommen Sie? Aus der Ukraine.",
    },
    {
        "word": "können",
        "translation": "могти, вміти",
        "example": "Ich kann Deutsch sprechen.",
    },
    {
        "word": "krank",
        "translation": "хворий",
        "example": "Ich bin heute krank.",
    },
    {
        "word": "lachen / das Leben",
        "translation": "сміятися / життя",
        "example": "Die Kinder lachen viel. Das Leben ist teuer.",
    },
    {
        "word": "lernen / lesen",
        "translation": "вчити / читати",
        "example": "Ich lerne Deutsch und lese ein Buch.",
    },
    {
        "word": "machen",
        "translation": "робити",
        "example": "Was machst du heute?",
    },
    {
        "word": "möchten / mögen",
        "translation": "хотіти б / любити",
        "example": "Was möchten Sie trinken? Magst du Kaffee?",
    },
    {
        "word": "müssen",
        "translation": "бути зобов'язаним, мусити",
        "example": "Ich muss arbeiten.",
    },
    {
        "word": "nehmen",
        "translation": "брати",
        "example": "Ich nehme den Bus.",
    },
    {"word": "neu", "translation": "новий", "example": "Wir haben eine neue Wohnung."},
    {
        "word": "öffnen / geöffnet",
        "translation": "відчиняти / відчинено",
        "example": "Der Laden ist geöffnet.",
    },
    {
        "word": "die Papiere / der Pass",
        "translation": "документи / паспорт",
        "example": "Haben Sie Ihre Papiere und den Pass dabei?",
    },
    {
        "word": "der Platz / das Problem",
        "translation": "місце / проблема",
        "example": "Der Platz ist besetzt. Kein Problem.",
    },
    {
        "word": "die Prüfung",
        "translation": "іспит",
        "example": "Die Prüfung ist am Montag.",
    },
    {
        "word": "pünktlich",
        "translation": "пунктуальний, вчасно",
        "example": "Der Zug fährt pünktlich.",
    },
    {
        "word": "reisen / reparieren",
        "translation": "подорожувати / ремонтувати",
        "example": "Ich reise gern. Er hat das Auto repariert.",
    },
    {
        "word": "richtig / ruhig",
        "translation": "правильно / тихий",
        "example": "Ist das richtig? Ich möchte ein ruhiges Zimmer.",
    },
    {
        "word": "sagen / die S-Bahn",
        "translation": "сказати / міська електричка",
        "example": "Können Sie mir das sagen? Ich nehme die S-Bahn.",
    },
    {
        "word": "schlafen / schlecht",
        "translation": "спати / погано",
        "example": "Ich schlafe gut. Mir ist schlecht.",
    },
    {
        "word": "schreiben / der Schreiber",
        "translation": "писати / письменник, ручка",
        "example": "Er schreibt einen Brief.",
    },
    {
        "word": "sehen / sprechen",
        "translation": "бачити / розмовляти",
        "example": "Ich sehe dich. Wir sprechen Deutsch.",
    },
    {
        "word": "stehen / die Straße",
        "translation": "стояти / вулиця",
        "example": "Der Bus steht an der Straße.",
    },
    {
        "word": "suchen / der Supermarkt",
        "translation": "шукати / супермаркет",
        "example": "Ich suche den Supermarkt.",
    },
    {
        "word": "tanzen / der Termin",
        "translation": "танцювати / зустріч, запис",
        "example": "Tanzen Sie gern? Ich habe einen Termin.",
    },
    {
        "word": "teuer / trinken",
        "translation": "дорогий / пити",
        "example": "Das ist zu teuer. Was willst du trinken?",
    },
    {
        "word": "umziehen",
        "translation": "переїжджати",
        "example": "Nächsten Monat ziehen wir um.",
    },
    {
        "word": "verstehen / verkaufen",
        "translation": "розуміти / продавати",
        "example": "Können Sie mich verstehen? Er verkauft das Auto.",
    },
    {
        "word": "warten / das Wasser",
        "translation": "чекати / вода",
        "example": "Können Sie kurz warten? Ein Glas Wasser, bitte.",
    },
    {
        "word": "wichtig / wissen",
        "translation":
