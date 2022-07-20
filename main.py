from config import open_weather_token
from pprint import pprint
import requests
import datetime

# ссылка на коды эмоджи https://unicode.org/emoji/charts/full-emoji-list.html

def get_weather(city, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )

        #http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid=c7cd39cc1dccfec3f6b49c3bca505b1f
        data = r.json()
        # pprint(data)

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


        print(f'*** {datetime.datetime.now().strftime("%Y--%m-%d %H:%M:%S")} ***\n'
              f'Погода в городе {city}\nТемпература: {temp}°C {wd}\n'
              f'Влажность: {humidity}\nВлажность: {pressure} мм.рт.ст\n'
              f'Ветер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_the_day}')

        return "Done"
    except Exception as ex:
        return 'Exception {ex}'

def main():
    #city = input("Enter the city")
    city = "moscow"
    print(get_weather(city, open_weather_token))

if __name__ == '__main__':
    main()