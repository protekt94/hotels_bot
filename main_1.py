from telebot import *
from pprint import pprint
#import lowprice
#import highprice
import bestdeal
# import history

token = '5546523733:AAGz1My1HV2VDnvhedZ7efgUBPfSK7GUlos'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup(row_width=1)
        low_price = types.InlineKeyboardButton(text='Топ самых дешёвых отелей', callback_data='/lowprice')
        high_price = types.InlineKeyboardButton(text='Топ самых дорогих отелей', callback_data='/highprice')
        best_deal = types.InlineKeyboardButton(text='Наиболее подходящие по цене и расположению от центра',
                                              callback_data='/bestdeal')
        history = types.InlineKeyboardButton(text='История поиска отелей', callback_data='/history')
        markup.add(low_price, high_price, best_deal, history)
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        # if call.data == '/lowprice':
        #     lowprice.hello_world(call.message)
        # elif call.data == '/highprice':
        #     highprice.hello_world(call.message)
        if call.data == '/bestdeal':
            bestdeal.hello_world(call.message)
        #elif call.data == '/history':
            #history.hello_world(call.message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
