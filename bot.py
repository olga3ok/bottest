import datetime
import telebot
from telebot import types
from config import TOKEN
import gspread
from yoomoney import Quickpay


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    # Создаю 4 кнопки для меню в начале работы с ботом
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Кнопка 1")
    btn2 = types.KeyboardButton("Кнопка 2")
    btn3 = types.KeyboardButton("Кнопка 3")
    btn4 = types.KeyboardButton("Кнопка 4")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я - бот для тестового задания.".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def func(message):
    if(message.text == "Кнопка 1"):
        # создаю кнопку с ссылкой на карты с адресом Ленина 1 в Москве
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Яндекс.Карты", url="https://yandex.ru/maps/213/moscow/house/ulitsa_lenina_1/Z04YdwFlT0ICQFtvfXpxcX1kZA==/?ll=37.165675%2C55.600171&z=16")
        markup.add(button1)
        bot.send_message(message.chat.id, "Нажми на кнопку и перейди на сайт Яндекс.Карт".format(message.from_user), reply_markup=markup)
    elif(message.text == "Кнопка 2"):
        # создаю кнопку с ссылкой на оплату 2р
        quickpay = Quickpay(
            receiver="410019014512803",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=2,
            )
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Ссылка на оплату ", url=quickpay.redirected_url)
        markup.add(button1)
        bot.send_message(message.chat.id, "Ссылка на оплату".format(message.from_user), reply_markup=markup)
    elif(message.text == "Кнопка 3"):
        # считываю изображение из файла и отправляю пользователю
        img = open("img1.jpg", "rb")
        # photo_url = 'https://ibb.co/MhNydZM'
        # bot.send_message(message.chat.id, photo_url)
        bot.send_photo(message.chat.id, img, caption="Картинка img1")
    elif(message.text == "Кнопка 4"):
        # получаю значение А2 из таблицы и отправляю его пользователю
        gc = gspread.service_account()
        sh = gc.open("гугл_табличка")
        text = sh.sheet1.acell("A2").value
        bot.send_message(message.chat.id, text=text)
    else:
        # проверяю введенное сообщение на соответствие формату даты дд.мм.гг
        try:
            date_format = "%d.%m.%Y"
            datetime.datetime.strptime(message.text, date_format)
            # если дата введена верно, записываю значение в столбец В таблицы
            gc = gspread.service_account()
            sh = gc.open("гугл_табличка")
            worksheet = sh.sheet1
            values_list = worksheet.col_values(2)
            worksheet.update_cell(len(values_list) + 1, 2, message.text)
            bot.send_message(message.chat.id, "Дата верна")
        except ValueError:
            bot.send_message(message.chat.id, "Дата неверна")


bot.infinity_polling()
