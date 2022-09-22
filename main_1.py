import requests
from telebot import *
from requests import *
from pprint import pprint
import lowprice
import highprice
import bestdeal

token = '5546523733:AAGz1My1HV2VDnvhedZ7efgUBPfSK7GUlos'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup(row_width=1)
        lowprice = types.InlineKeyboardButton(text='Топ самых дешёвых отелей', callback_data='/lowprice')
        highprice = types.InlineKeyboardButton(text='Топ самых дорогих отелей', callback_data='/highprice')
        bestdeal = types.InlineKeyboardButton(text='Наиболее подходящие по цене и расположению от центра',
                                              callback_data='/bestdeal')
        history = types.InlineKeyboardButton(text='История поиска отелей', callback_data='/history')
        markup.add(lowprice, highprice, bestdeal, history)
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == '/lowprice':
            lowprice.hello_world(call.message)
            if call.data == 'no':
                for num_hotel in range(int()):
                    name, star_rating, current_price = lowprice.info_hotels(num_hotel)
                    bot.send_message(call.message.chat.id,
                                     f'Name: {name}\n'
                                     f'Star rating: {star_rating}\n'
                                     f'Current price: {current_price}'
                                     )
            elif call.data == 'yes':
                bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
                bot.register_next_step_handler(call.message, lowprice.get_numbers_photo)
        elif call.data == '/highprice':
            highprice.hello_world(call.message)
            if call.data == 'no':
                for num_hotel in range(int()):
                    name, star_rating, current_price = highprice.info_hotels(num_hotel)
                    bot.send_message(call.message.chat.id,
                                     f'Name: {name}\n'
                                     f'Star rating: {star_rating}\n'
                                     f'Current price: {current_price}'
                                     )
            elif call.data == 'yes':
                bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
                bot.register_next_step_handler(call.message, highprice.get_numbers_photo)
        elif call.data == '/bestdeal':
            bestdeal.hello_world(call.message)
            if call.data == 'no':
                for num_hotel in range(int()):
                    name, star_rating, current_price = bestdeal.info_hotels(num_hotel)
                    bot.send_message(call.message.chat.id,
                                     f'Name: {name}\n'
                                     f'Star rating: {star_rating}\n'
                                     f'Current price: {current_price}'
                                     )
            elif call.data == 'yes':
                bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
                bot.register_next_step_handler(call.message, bestdeal.get_numbers_photo)
    # elif call.data == '/history':
    # 	history.hello_world(call.message)
    # 	if call.data == 'no':
    # 		for num_hotel in range(int()):
    # 			name, star_rating, current_price = history.info_hotels(num_hotel)
    # 			bot.send_message(call.message.chat.id,
    # 							 f'Name: {name}\n'
    # 							 f'Star rating: {star_rating}\n'
    # 							 f'Current price: {current_price}'
    # 							 )
    # 	elif call.data == 'yes':
    # 		bot.send_message(call.from_user.id, 'Сколько фото отеля показать? (не больше 10)')
    # 		bot.register_next_step_handler(call.message, history.get_numbers_photo)


bot.polling(none_stop=True)
