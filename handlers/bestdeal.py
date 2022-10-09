import json

from aiogram import Router, F, types
from aiogram.filters.text import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from keyboards.for_questions import get_yes_no_kb
import requests
import datetime
from handlers.questions import BotDB

router = Router()


class OrderFood(StatesGroup):
    """
    Класс, который создает состояние для функций
    """
    get_date_departures = State()
    get_date_arrival = State()
    get_city = State()
    get_number_hotels = State()
    get_numbers_photo = State()
    get_price_min = State()
    get_price_max = State()
    get_distance_max = State()
    get_yes_no = State()


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
count_night = ''
photos = []


@router.message(Command(commands=("bestdeal", "b"), commands_prefix="/!"))
@router.callback_query(Text(text='/bestdeal'))
async def hello_world(message: types.Message, state: FSMContext):
    """
    Функция поиска отелей по цене и удалению от цента
    :param message: bestdeal
    :param state: состояние
    :return: None
    """
    await callback.answer()
    await message.answer(text='Введите название города где будет проводиться поиск')
    await state.set_state(OrderFood.get_city)

    def get_photo(hotel):
        """
        Функция получения фото по id отеля
        :param hotel: id отеля
        :return: список из ссылок на фото
        """
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
        """
        Функция получения id города
        :param city: Название города
        :return: id города
        """
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": city, "locale": "en_US", "currency": "USD"}
        headers = {
            "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        destinationId = data['suggestions'][0]['entities'][0]['destinationId']
        print(f'Получил номер города - {destinationId}')
        return destinationId

    def get_all_hotels(destination, date_arrival, date_departures, price_min, price_max):
        """
        Функция получения списка отелей
        :param destination: id города
        :param date_departures: дата приезда в отель
        :param date_arrival: дата отъезда из отеля
        :param price_min: минимальная цена
        :param price_max: максимальная цена
        :return: список id отелей
        """
        global count_night
        print('Получил номера всех отелей')
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": destination, "pageNumber": "1", "pageSize": "25",
                       "checkIn": date_departures,
                       "checkOut": date_arrival, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                       "sortOrder": "PRICE", "locale": "en_US",
                       "currency": "USD"}
        headers = {
            "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        count_night = datetime.datetime.strptime(date_departures, '%Y-%m-%d') - datetime.datetime.strptime(date_arrival,
                                                                                                           '%Y-%m-%d')
        return data

    def get_hotels(id_hotel, date_arrival, date_departures):
        """
        Функция, которая получает информацию отеля
        :param id_hotel: id отеля
        :param date_arrival: дата заезда
        :param date_departures: дата отъезда
        :return: информация об отеле
        """
        url = "https://hotels4.p.rapidapi.com/properties/get-details"
        querystring = {"id": id_hotel, "checkIn": date_arrival, "checkOut": date_departures, "adults1": "1",
                       "currency": "USD",
                       "locale": "ru_RU"}
        headers = {
            "X-RapidAPI-Key": "d7cc18d44bmsha3ef602e9b7e9f3p1e4b7fjsnc9c3d139d967",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        print('Получил нужный отель')
        return data

    @router.message(OrderFood.get_city, F.text)
    async def get_city(message: Message, state: FSMContext):
        """
        Функция проверки города
        :param message: город
        :param state: состояние
        :return: None
        """
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
        """
        Функция получения даты заселения
        :param message: дата заселения в формате yyyy-mm-dd
        :param state: состояние
        :return: None
        """
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
        """
        Функция получения даты выезда
        :param message: дата выезда в формате yyyy-mm-dd
        :param state: состояние
        :return: None
        """
        global date_arrival, get_hotel
        date_arrival = message.text
        try:
            datetime.datetime.strptime(date_arrival, '%Y-%m-%d')
            print(f'Дата возвращения - {date_arrival}')
            await message.answer(text='Минимальная стоимость отела за одну ночь: ')
            await state.set_state(OrderFood.get_price_min)
        except ValueError:
            await message.answer(text='Вы ввели неправильный формат даты. Попробуйте еще раз')
            await state.set_state(OrderFood.get_date_arrival)

    @router.message(OrderFood.get_price_min, F.text)
    async def get_price_min(message: Message, state: FSMContext):
        """
        Функция получения минимальной стоимости отеля
        :param message: минимальная стоимость отеля
        :param state: состояние
        :return: None
        """
        global price_min
        price_min = message.text
        try:
            price_min.isdigit()
            print(f'Минимальная стоимость - {price_min}')
            await message.answer(text='Максимальная стоимость отела за одну ночь: ')
            await state.set_state(OrderFood.get_price_max)
        except ValueError:
            await message.answer(text='Вы ввели не число. Попробуйте еще раз')
            await state.set_state(OrderFood.get_price_min)

    @router.message(OrderFood.get_price_max, F.text)
    async def get_price_max(message: Message, state: FSMContext):
        """
        Функция получения максимальной стоимости отеля
        :param message: максимальная стоимость отеля
        :param state: состояние
        :return: None
        """
        global price_max
        price_max = message.text
        print(f'Максимальная стоимость - {price_max}')
        try:
            price_max.isdigit()
            await message.answer(text='Максимальное расстояние от центра: ')
            await state.set_state(OrderFood.get_distance_max)
        except ValueError:
            await message.answer(text='Вы ввели не число. Попробуйте еще раз')
            await state.set_state(OrderFood.get_price_max)

    @router.message(OrderFood.get_distance_max, F.text)
    async def get_distance_max(message: Message, state: FSMContext):
        """
        Функция, которая определяет максимальное отдаление от центра города
        :param message: максимальное расстояние от центра
        :param state: состояние
        :return: None
        """
        global distance_max
        distance_max = message.text
        try:
            price_max.isdigit()
            print(f'Максимальное расстояние - {distance_max}')
            await message.answer(text='Сколько отелей вывести в результате (не больше 25)')
            await state.set_state(OrderFood.get_number_hotels)
        except ValueError:
            await message.answer(text='Вы ввели не число. Попробуйте еще раз')
            await state.set_state(OrderFood.get_distance_max)
        finally:
            get_distance()

    @router.message(OrderFood.get_number_hotels, F.text)
    async def get_number_hotels(message: Message, state: FSMContext):
        """
        Функция получения кол-ва отелей
        :param message: кол-во отелей, которое необходимо вывести
        :param state: состояние
        :return: None
        """
        global numbers_hotels
        numbers_hotels = message.text
        if 25 > int(numbers_hotels) > 0:
            await message.answer('Нужно ли вывести фото отелей?', reply_markup=get_yes_no_kb())
            await state.set_state(OrderFood.get_yes_no)
        else:
            await message.answer(text='Вы ввели недопустимое число. Попробуйте еще раз!')
            await state.set_state(OrderFood.get_number_hotels)

    @router.message(OrderFood.get_numbers_photo, F.text)
    async def get_numbers_photo(message: types.Message, state: FSMContext):
        """
        Функция вывода фото отеля
        :param message: кол-во фото, которое необходимо вывести
        :param state: состояние
        :return: None
        """
        global price_hotel, numbers_hotels, numbers_photo, count_night, photos
        numbers_photo = message.text
        if 9 < int(numbers_photo) <= 0:
            await message.answer(text='Вы ввели недопустимое число. Попробуйте еще раз!')
            await state.set_state(OrderFood.get_number_hotels)
        else:
            await state.set_state(state=None)
            for id_hotel in price_hotel[:int(numbers_hotels)]:
                name, star_rating, current_price = info_hotels(id_hotel)
                photos = []
                all_photo = get_photo(id_hotel)
                for num_photo in range(0, int(numbers_photo)):
                    urls = all_photo['hotelImages'][num_photo]['baseUrl']
                    new_url = urls.replace('_{size}', '')
                    photos.append(new_url)
                photos_dumps = json.dumps(photos)
                media = []
                for i_photo in photos:
                    if i_photo == photos[0]:
                        media.append(types.InputMediaPhoto(type='photo', media=i_photo, caption=
                        f'Name: {name}\n '
                        f'Star rating: {star_rating}\n'
                        f'Current price: {current_price}'
                                                           ))
                    else:
                        media.append(types.InputMediaPhoto(type='photo', media=i_photo))
                await message.answer_media_group(media=media)
                BotDB.add_record(message.chat.id, name, star_rating, current_price, photos_dumps)

    def info_hotels(id_hotel):
        """
        Функция вывода информации о отеле
        :param id_hotel: id отеля
        :return: Имя отеля, рейтинг, цена
        """
        global date_arrival, date_departures, get_hotel
        get_hotel = get_hotels(id_hotel, date_arrival, date_departures)
        name = get_hotel['data']['body']['propertyDescription']['name']
        star_rating = get_hotel['data']['body']['propertyDescription']['starRating']
        current_price = get_hotel['data']['body']['propertyDescription']['featuredPrice']['currentPrice']['formatted']
        return name, star_rating, current_price

    def get_distance():
        """
        Функция, которая выбирает отели подходящие под нужное расстояние от центра
        :return: None
        """
        global get_all_hotel, distance_max, price_hotel, destination, date_arrival, date_departures, price_min, \
            price_max
        get_all_hotel = get_all_hotels(destination, date_arrival, date_departures, price_min, price_max)
        for num_hotel in range(25):
            distance = get_all_hotel['data']['body']['searchResults']['results'][num_hotel]['landmarks'][0][
                'distance'].split()
            id_hotel = get_all_hotel['data']['body']['searchResults']['results'][num_hotel]['id']
            if float(distance[0]) <= float(distance_max):
                price_hotel.append(id_hotel)

    @router.callback_query(Text(text="yes"), OrderFood.get_yes_no)
    async def callback(callback: types.CallbackQuery, state: FSMContext):
        """
          Функция вывода информации с фото
          :param callback: Ответ "Да"
          :param state: состояние
          :return: None
          """
        message = callback.message
        await message.answer(text='Сколько фото отеля показать? (не больше 10)')
        await state.set_state(OrderFood.get_numbers_photo)

    @router.callback_query(Text(text="no"), OrderFood.get_yes_no)
    async def callback(callback: types.CallbackQuery):
        """
          Функция вывода информации без фото
          :param callback: Ответ "Нет"
          :param state: состояние
          :return: None
          """
        global numbers_hotels, price_hotel
        print(price_hotel)
        message = callback.message
        for id_hotel in price_hotel[:int(numbers_hotels)]:
            name, star_rating, current_price = info_hotels(id_hotel)
            BotDB.add_record(message.chat.id, name, star_rating, current_price, None)
            await message.answer(text=f'Name: {name}\n '
                                      f'Star rating: {star_rating}\n'
                                      f'Total {current_price} for {count_night} nights'
                                 )
            await state.set_state(state=None)
            break
