import requests
from telebot import *

city = ''
destination = ''
numbers_hotels = ''
numbers_photo = ''
date_arrival = ''
date_departures = ''
get_all_hotel = ''
get_hotel = ''
price_min = ''
price_max = ''
distance_max = ''
price_hotel = []

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
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "en_US", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    destinationId = data['suggestions'][0]['entities'][0]['destinationId']
    print(f'Получил номер города - {destinationId}')
    return destinationId


def get_all_hotels(destination, date_arrival, date_departures, price_min, price_max):
    print('Получил номера всех отелей')
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination, "pageNumber": "1", "pageSize": "25",
                   "checkIn": date_departures,
                   "checkOut": date_arrival, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                   "sortOrder": "PRICE", "locale": "en_US",
                   "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def get_hotels(id_hotel, date_arrival, date_departures):
    print('Получил нужный отель')
    url = "https://hotels4.p.rapidapi.com/properties/get-details"
    querystring = {"id": id_hotel, "checkIn": date_arrival, "checkOut": date_departures, "adults1": "1", "currency": "USD",
                   "locale": "ru_RU"}
    headers = {
        "X-RapidAPI-Key": "b6cc945013msh856c589e4a74642p165b64jsn59491bf0087b",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


@bot.message_handler(content_types=['text'])
def hello_world(call):
    bot.send_message(call.chat.id, 'Введите название города где будет проводиться поиск')
    bot.register_next_step_handler(call, get_city)


@bot.message_handler(content_types=['text'])
def get_city(message):
    global city, destination
    city = message.text
    print(f'Город - {city}')
    destination = get_destinationId(city)
    bot.send_message(message.from_user.id, 'Введите дату приезда в формате yyyy-mm-dd')
    bot.register_next_step_handler(message, get_date_arrival)


@bot.message_handler(content_types=['text'])
def get_date_arrival(message):
    global date_arrival
    date_arrival = message.text
    print(f'Дата прибытия - {date_arrival}')
    bot.send_message(message.from_user.id, 'Введите дату отъезда в формате yyyy-mm-dd')
    bot.register_next_step_handler(message, get_date_departure)


@bot.message_handler(content_types=['text'])
def get_date_departure(message):
    global date_departures
    date_departures = message.text
    print(f'Дата возвращения - {date_departures}')
    bot.send_message(message.from_user.id, 'Минимальная стоимость отела: ')
    bot.register_next_step_handler(message, get_price_min)


@bot.message_handler(content_types=['text'])
def get_price_min(message):
    global price_min
    price_min = message.text
    print(f'Минимальная цена - {price_min}')
    bot.send_message(message.from_user.id, 'Максимальная стоимость отела: ')
    bot.register_next_step_handler(message, get_price_max)


@bot.message_handler(content_types=['text'])
def get_price_max(message):
    global price_max
    price_max = message.text
    print(f'Максимальная цена - {price_max}')
    bot.send_message(message.from_user.id, 'Максимальное расстояние от центра: ')
    bot.register_next_step_handler(message, get_distance_max)


@bot.message_handler(content_types=['text'])
def get_distance_max(message):
    global distance_max
    distance_max = message.text
    print(f'Максимальное расстояние - {distance_max}')
    bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10): ')
    bot.register_next_step_handler(message, get_number_hotels)


@bot.message_handler(content_types=['text'])
def get_number_hotels(message):
    global numbers_hotels
    numbers_hotels = message.text
    # if numbers_hotels.isdigit():
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_yes, key_no)
    question = 'Нужно ли вывести фото отелей?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    # else:
    #     bot.send_message(message.from_user.id, 'Вы ввели не число. Попробуйте еще раз!')
    #     bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате (не больше 10)')
    #     bot.register_next_step_handler(message, get_number_hotels)


@bot.message_handler(content_types=['text'])
def get_numbers_photo(message):
    global numbers_photo, numbers_hotels, get_hotel
    numbers_photo = message.text
    if int(numbers_photo) > 10 or int(numbers_photo) <= 0:
        bot.send_message(message.from_user.id, 'Вы ввели недопустимое число. Попробуйте еще раз!')
        get_numbers_photo(message)
    else:
        for id_hotel in price_hotel[:int(numbers_hotels)]:
            name, star_rating, current_price = info_hotels(id_hotel)
            photos = []
            all_photo = get_photo(id_hotel)
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


def info_hotels(id_hotel):
    global get_hotel, date_arrival, date_departures
    get_hotel = get_hotels(id_hotel, date_arrival, date_departures)
    name = get_hotel['data']['body']['propertyDescription']['name']
    star_rating = get_hotel['data']['body']['propertyDescription']['starRating']
    current_price = get_hotel['data']['body']['propertyDescription']['featuredPrice']['currentPrice']['formatted']
    return name, star_rating, current_price


def get_distance():
    global get_all_hotel, distance_max, price_hotel
    get_all_hotel = get_all_hotels(destination, date_arrival, date_departures, price_min, price_max)
    for num_hotel in range(25):
        distance = get_all_hotel['data']['body']['searchResults']['results'][num_hotel]['landmarks'][0][
            'distance'].split()
        id_hotel = get_all_hotel['data']['body']['searchResults']['results'][num_hotel]['id']
        if float(distance[0]) <= float(distance_max):
            price_hotel.append(id_hotel)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global get_all_hotel
    if call.message:
        get_distance()
        if call.data == 'no':
            for num_hotel in range(int(numbers_hotels)):
                name, star_rating, current_price = info_hotels()
                bot.send_message(call.message.chat.id,
                                 f'Name: {name}\n'
                                 f'Star rating: {star_rating}\n'
                                 f'Current price: {current_price}'
                                 )
        elif call.data == 'yes':
            bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
            bot.register_next_step_handler(call.message, get_numbers_photo)


bot.polling(none_stop=True)
