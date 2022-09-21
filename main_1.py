from telebot import *
import requests
from pprint import pprint

city = ''
numbers_hotels = ''
date_arrival = ''
date_departures = ''


def get_destinationId(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "en_US", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "dbaecd57a7msh566615f43b1c60fp1a7d2ejsnea445d8973bd",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    destinationId = data['suggestions'][0]['entities'][0]['destinationId']
    print(destinationId)
    # return destinationId


def get_hotels(city):
    global numbers_hotels, date_arrival, date_departures
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": get_destinationId(city), "pageNumber": "1", "pageSize": numbers_hotels,
                   "checkIn": date_departures,
                   "checkOut": date_arrival, "adults1": "1", "sortOrder": "PRICE_HIGHEST_FIRST", "locale": "en_US",
                   "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "dbaecd57a7msh566615f43b1c60fp1a7d2ejsnea445d8973bd",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()



token = '5546523733:AAGz1My1HV2VDnvhedZ7efgUBPfSK7GUlos'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup(row_width=1, )
        lowprice = types.InlineKeyboardButton(text='Топ самых дешёвых отелей', callback_data='/lowprice')
        highprice = types.InlineKeyboardButton(text='Топ самых дорогих отелей', callback_data='/highprice')
        bestdeal = types.InlineKeyboardButton(text='Топ отелей, наиболее подходящих по цене и расположению от центра',
                                              callback_data='/bestdeal')
        history = types.InlineKeyboardButton(text='История поиска отелей', callback_data='/history')
        markup.add(lowprice, highprice, bestdeal, history)
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def hello_world(call):
    bot.send_message(call.chat.id, 'Введите название города где будет проводиться поиск',parse_mode='html')
    bot.register_next_step_handler(call, get_date_departures)


@bot.message_handler(content_types=['text'])
def get_date_departures(message):
    global city
    city = message.text

    bot.send_message(message.from_user.id, 'Введите дату вылета в формате yyyy-mm-dd')
    bot.register_next_step_handler(message, get_date_arrival)


@bot.message_handler(content_types=['text'])
def get_date_arrival(message):
    global date_departures
    date_departures = message.text
    bot.send_message(message.from_user.id, 'Введите дату прибытия в формате yyyy-mm-dd')
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types=['text'])
def get_city(message):
    global date_arrival
    date_arrival = message.text
    bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10)')
    bot.register_next_step_handler(message, get_number_hotels)


@bot.message_handler(content_types=['text'])
def get_number_hotels(message):
    global numbers_hotels
    numbers_hotels = message.text
    if numbers_hotels.isdigit():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)
        question = 'Нужно ли вывести фото отелей?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Вы ввели не число. Попробуйте еще раз!')
        bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10)')
        bot.register_next_step_handler(message, get_number_hotels)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == '/lowprice':
            hello_world(call.message)
        if call.data == 'no':
            print(city)
            get_hotels(city)


bot.polling(none_stop=True)
