import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет, напиши мне название города и я посмотрю какая там погода")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )

        # http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid=c7cd39cc1dccfec3f6b49c3bca505b1f
        data = r.json()

        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Бро, погляди в окно, мне трудно сказать что там"

        await message.reply(f'*** {datetime.datetime.now().strftime("%Y--%m-%d %H:%M:%S")} ***\n'
              f'Погода в городе {city}\nТемпература: {temp}°C {wd}\n'
              f'Влажность: {humidity}\nВлажность: {pressure} мм.рт.ст\n'
              f'Ветер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_the_day}')
    except Exception as ex:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == "__main__":
    executor.start_polling(dp)