import requests
from telebot import *

city = ''
destination = ''
numbers_hotels = ''
numbers_photo = ''
date_arrival = ''
date_departures = ''
get_hotel = ''


token = '5546523733:AAGz1My1HV2VDnvhedZ7efgUBPfSK7GUlos'
bot = telebot.TeleBot(token)


def get_photo(hotel):
    print('Получил фото отеля')
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def get_destinationId(city):
    print('Получил номер города')
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    destinationId = data['suggestions'][0]['entities'][0]['destinationId']
    return destinationId


def get_hotels(destination, numbers_hotels, date_arrival, date_departures):
    print('Получил номер отеля')

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination, "pageNumber": "1", "pageSize": numbers_hotels,
                   "checkIn": date_departures,
                   "checkOut": date_arrival, "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU",
                   "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


@bot.message_handler(content_types=['text'])
def hello_world(message):
    bot.send_message(message.chat.id, 'Введите название города где будет проводиться поиск')
    bot.register_next_step_handler(message, get_date_departures)


@bot.message_handler(content_types=['text'])
def get_date_departures(message):
    global city, destination
    city = message.text
    try:
        destination = get_destinationId(city)
        bot.send_message(message.from_user.id, 'Введите дату приезда в формате yyyy-mm-dd')
        bot.register_next_step_handler(message, get_date_arrival)
    except:
        bot.send_message(message.from_user.id, 'Такого города нет в базе. Попробуйте еще раз!')
        bot.register_next_step_handler(message, get_date_departures)


@bot.message_handler(content_types=['text'])
def get_date_arrival(message):
    global date_departures
    date_departures = message.text
    bot.send_message(message.from_user.id, 'Введите дату отъезда в формате yyyy-mm-dd')
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types=['text'])
def get_city(message):
    global date_arrival, get_hotel
    date_arrival = message.text
    get_hotel = get_hotels(destination, numbers_hotels, date_arrival, date_departures)
    bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10)')
    bot.register_next_step_handler(message, get_number_hotels)


@bot.message_handler(content_types=['text'])
def get_number_hotels(message):
    global numbers_hotels
    numbers_hotels = message.text
    if numbers_hotels.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)
        question = 'Нужно ли вывести фото отелей?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Вы ввели не число. Попробуйте еще раз!')
        bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10)')
        bot.register_next_step_handler(message, get_number_hotels)


@bot.message_handler(content_types=['text'])
def get_numbers_photo(message):
    global numbers_photo, numbers_hotels
    numbers_photo = message.text
    if int(numbers_photo) > 10 or int(numbers_photo) <= 0:
        bot.send_message(message.from_user.id, 'Вы ввели недопустимое число. Попробуйте еще раз!')
        get_numbers_photo(message)
    else:
        for num_hotel in range(0, int(numbers_hotels)):
            photos = []
            get_hotel_photo = get_hotels(destination, numbers_hotels, date_arrival, date_departures)
            name, star_rating, current_price = info_hotels(num_hotel)
            hotel = get_hotel_photo['data']['body']['searchResults']['results'][num_hotel]['id']
            all_photo = get_photo(hotel)
            for num_photo in range(0, int(numbers_photo)):
                urls = all_photo['hotelImages'][num_photo]['baseUrl']
                new_url = urls.replace('_{size}', '')
                photos.append(new_url)
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(photo) for photo in photos])
            bot.send_message(message.from_user.id,
                             f'Name: {name}\n'
                             f'Star rating: {star_rating}\n'
                             f'Current price: {current_price}'
                             )


def info_hotels(number_hotel):
    global get_hotel
    name = get_hotel['data']['body']['searchResults']['results'][number_hotel]['name']
    star_rating = get_hotel['data']['body']['searchResults']['results'][number_hotel]['starRating']
    current_price = get_hotel['data']['body']['searchResults']['results'][number_hotel]['ratePlan']['price']['current']
    return name, star_rating, current_price


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'no':
            for num_hotel in range(int(numbers_hotels)):
                name, star_rating, current_price = info_hotels(num_hotel)
                bot.send_message(call.message.chat.id,
                                 f'Name: {name}\n'
                                 f'Star rating: {star_rating}\n'
                                 f'Current price: {current_price}'
                                 )
        elif call.data == 'yes':
            bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
            bot.register_next_step_handler(call.message, get_numbers_photo)


bot.polling(none_stop=True)
