import json

from aiogram import Router, F, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from keyboards.for_questions import get_yes_no_kb
import requests
import datetime
from handlers.questions import BotDB

router = Router()

city = ''
destination = ''
numbers_hotels = ''
numbers_photo = ''
date_arrival = ''
date_departures = ''
get_hotel = ''
get_price = ''
photos = []


class OrderFood(StatesGroup):
    get_date_departures = State()
    get_date_arrival = State()
    get_city = State()
    get_number_hotels = State()
    get_numbers_photo = State()


def get_photo(hotel):
    print('Получил фото отеля')
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel}
    headers = {
        "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def get_destination_id(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    destinationId = data['suggestions'][0]['entities'][0]['destinationId']
    print(f'Получил номер города - {destinationId}')
    return destinationId


def get_hotels(destination, numbers_hotels, date_departures, date_arrival, price):
    print('Получил номера всех отелей')
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination, "pageNumber": "1", "pageSize": numbers_hotels,
                   "checkIn": date_departures,
                   "checkOut": date_arrival, "adults1": "1", "sortOrder": price, "locale": "ru_RU",
                   "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


user_data = {}


@router.callback_query(Text(text_endswith='price'))
async def hello_world(callback: types.CallbackQuery, state: FSMContext):
    global get_price
    message = callback.message
    if callback.data == '/lowprice':
        get_price = 'PRICE'
    elif callback.data == '/highprice':
        get_price = 'PRICE_HIGHEST_FIRST'
    await message.answer(text='Введите название города где будет проводиться поиск')
    await state.set_state(OrderFood.get_city)

    @router.message(OrderFood.get_city, F.text)
    async def get_city(message: Message, state: FSMContext):
        global city, destination
        city = message.text
        print(f'Город - {city}')
        try:
            destination = get_destination_id(city)
            await message.answer(text='Введите дату приезда в формате yyyy-mm-dd')
            await state.set_state(OrderFood.get_date_departures)
        except IndexError:
            await message.answer(text='Такого города нет в базе. Попробуйте еще раз!')
            await state.set_state(OrderFood.get_city)

    @router.message(OrderFood.get_date_departures, F.text)
    async def get_date_departures(message: Message, state: FSMContext):
        global date_departures
        date_departures = message.text
        try:
            datetime.datetime.strptime(date_departures, '%Y-%m-%d')
            print(f'Дата прибытия - {date_departures}')
            await message.answer(text='Введите дату отъезда в формате yyyy-mm-dd')
            await state.set_state(OrderFood.get_date_arrival)
        except ValueError:
            await message.answer(text='Вы ввели неправильный формат даты. Попробуйте еще раз')
            await state.set_state(OrderFood.get_date_departures)

    @router.message(OrderFood.get_date_arrival, F.text)
    async def get_date_arrival(message: Message, state: FSMContext):
        global date_arrival, get_hotel, get_price, numbers_hotels, destination, date_departures
        date_arrival = message.text
        try:
            datetime.datetime.strptime(date_arrival, '%Y-%m-%d')
            print(f'Дата возвращения - {date_arrival}')
            get_hotel = get_hotels(destination, numbers_hotels, date_departures, date_arrival, get_price)
            await message.answer(text='Сколько отелей вывести в результате (не больше 25)')
            await state.set_state(OrderFood.get_number_hotels)
        except ValueError:
            await message.answer(text='Вы ввели неправильный формат даты. Попробуйте еще раз')
            await state.set_state(OrderFood.get_date_arrival)

    @router.message(OrderFood.get_number_hotels, F.text)
    async def get_number_hotels(message: Message, state: FSMContext):
        global numbers_hotels
        numbers_hotels = message.text
        if int(numbers_hotels) < 25 or int(numbers_hotels) > 0:
            await message.answer('Нужно ли вывести фото отелей?', reply_markup=get_yes_no_kb())
        else:
            await message.answer(text='Вы ввели недопустимое число. Попробуйте еще раз!')
            await state.set_state(OrderFood.get_number_hotels)

    @router.message(OrderFood.get_numbers_photo, F.text)
    async def get_numbers_photo(message: Message, state: FSMContext):
        global numbers_photo, numbers_hotels, get_hotel, photos
        numbers_photo = message.text
        if 9 < int(numbers_photo) <= 0:
            await message.answer(text='Вы ввели недопустимое число. Попробуйте еще раз!')
            await state.set_state(OrderFood.get_number_hotels)
        else:
            for num_hotel in range(0, int(numbers_hotels)):
                photos = []
                name, star_rating, current_price = info_hotels(num_hotel)
                hotel = get_hotel['data']['body']['searchResults']['results'][num_hotel]['id']
                all_photo = get_photo(hotel)
                for num_photo in range(0, int(numbers_photo)):
                    urls = all_photo['hotelImages'][num_photo]['baseUrl']
                    new_url = urls.replace('_{size}', '')
                    photos.append(new_url)
                photos_dumps = json.dumps(photos)
                BotDB.add_record(message.chat.id, name, star_rating, current_price, photos_dumps)
                await message.answer_media_group(media=[types.InputMediaPhoto(media=photo) for photo in photos])
                await message.answer(text=f'Name: {name}\n'
                                          f'Star rating: {star_rating}\n'
                                          f'Current price: {current_price}'
                                     )

    def info_hotels(number_hotel):
        global get_hotel
        name = get_hotel['data']['body']['searchResults']['results'][number_hotel]['name']
        star_rating = get_hotel['data']['body']['searchResults']['results'][number_hotel]['starRating']
        current_price = get_hotel['data']['body']['searchResults']['results'][number_hotel]['ratePlan']['price'][
            'current']
        return name, star_rating, current_price

    @router.callback_query(Text(text="yes"))
    async def callback(callback: types.CallbackQuery, state: FSMContext):
        message = callback.message
        await message.answer(text='Сколько фото отеля показать? (не больше 10)')
        await state.set_state(OrderFood.get_numbers_photo)

    @router.callback_query(Text(text="no"))
    async def callback(callback: types.CallbackQuery):
        global numbers_hotels
        message = callback.message
        for num_hotel in range(int(numbers_hotels)):
            name, star_rating, current_price = info_hotels(num_hotel)
            BotDB.add_record(message.chat.id, name, star_rating, current_price, None)
            await message.answer(text=f'Name: {name}\n '
                                      f'Star rating: {star_rating}\n'
                                      f'Current price: {current_price}'
                                 )
