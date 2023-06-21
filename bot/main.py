from aiogram import Bot,Dispatcher,executor,types
import logging
import redis
import psycopg2
from main_vars import vars
import pandas as pd
from matplotlib import pyplot as plt
import io
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = vars.API_TOKEN

logging.basicConfig(level=logging.INFO)

order_column_names = ['id','pay_type','address','created','email','first_name','last_name']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

r = redis.Redis(host='localhost',port=6379,decode_responses=True)
connection = psycopg2.connect(host="localhost",
    port=5432,
    database="delivery",
    user="delivery",
    password=vars.DB_PASSWORD)

cursor = connection.cursor()

admin_ids = [811338310,]

@dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm My Delivery bot\nYou can get status of your order\nJust send id of your order.")


@dp.message_handler(commands='get_statistics')
async def get_statistics(message: types.Message):
    if message.from_user.id in admin_ids:
        most_paytype_button = InlineKeyboardButton(text='Most Pay type',callback_data='most_paytype_stat')
        last_10days_order_count_button = InlineKeyboardButton(text='Order count from last 10 days',callback_data='last_10days_order_count')
        new_user_count_button = InlineKeyboardButton(text='New users of last year',callback_data='new_user_count')
        keyboard_inline = InlineKeyboardMarkup().add(most_paytype_button,last_10days_order_count_button,new_user_count_button)
        
        await message.reply('Choose statistics',reply_markup=keyboard_inline)
        
    else:
        await message.reply("You are not admin.")

@dp.callback_query_handler(text=['new_user_count'])
async def new_user_count_handler(call: types.CallbackQuery):

    cursor.execute("SELECT date_joined FROM customer_customer WHERE date_joined > (CURRENT_DATE - interval '1 year')")
    users_data = cursor.fetchall()

    users_DataFrame = pd.DataFrame(users_data,columns=['date_joined'])
    users_DataFrame['date_joined'] = pd.to_datetime(users_DataFrame['date_joined'])
    print(users_DataFrame)
    lastyear_users = users_DataFrame.groupby(users_DataFrame['date_joined'].dt.month).size()
    
    lastyear_users.plot.bar(xlabel='month',ylabel='count',rot=0)
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer,format='png')
    image_buffer.seek(0)

    await bot.send_photo(call.message.chat.id, photo=image_buffer)

@dp.callback_query_handler(text=['most_paytype_stat'])
async def most_paytype_stat_handler(call: types.CallbackQuery):

    cursor.execute("SELECT * FROM delivery_order")
    order_data = cursor.fetchall()

    order_DataFrame = pd.DataFrame(order_data,columns=order_column_names)
    value_counts = order_DataFrame['pay_type'].value_counts()
    percentage = value_counts / len(order_DataFrame) * 100
    percentage.plot.bar(x='Pay type', y='percent',rot=0)
    
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer,format='png')
    image_buffer.seek(0)

    await bot.send_photo(call.message.chat.id, photo=image_buffer)

@dp.callback_query_handler(text=['last_10days_order_count'])
async def most_paytype_stat_handler(call: types.CallbackQuery):
    cursor.execute("SELECT * FROM delivery_order WHERE created > (CURRENT_DATE - interval '10 days')")
    order_data = cursor.fetchall()

    df = pd.DataFrame(order_data, columns=order_column_names)
    df['created'] = pd.to_datetime(df['created'])
    daily_orders = df.groupby(df['created'].dt.day).size()

    daily_orders.plot.bar(y='count')
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer,format='png')
    image_buffer.seek(0)
    await bot.send_photo(call.message.chat.id, photo=image_buffer)

@dp.message_handler()
async def get_status(message: types.Message):
    status = r.get(f'order:{message.text}:status')
    if status:
        await message.reply(f"Status of your order: {status}")
    else:
        await message.reply("Order not found.")



if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)