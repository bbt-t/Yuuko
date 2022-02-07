<p align="center">
  <img alt="" src="https://i.ibb.co/FX1jp6H/preview-logo.webp" width="500px">
</p>

[:us: English version](README_en.md)
### О боте

>Телеграм бот на асинхронной библиотеке aiogram v2.x, поддерживает 2 языка [RU, EN]


<details>
 <summary>Что может бот на сегодня</summary>
<ul>
  <li>Оповестить о погоде :heavy_check_mark:</li>
  <li>Напомнить о делах :heavy_check_mark:</li>
  <li>Сохранять пароли :heavy_check_mark:</li>
  <li>Узнать какие дни "удачные" для стрижки :heavy_check_mark:</li>
  <li>Получить гороскоп :heavy_check_mark:</li>
  <li>Распознать текст на фото ️:warning:</li>
</ul>
</details>

***

### Запуск
Собрать `docker-контейнер` и запустить:
```
docker build -t bot-pet .
docker run -p 8000:8000 --name bot bot-pet:latest 
```
или без docker'a:
```
python start.py
```

***

### ВАЖНО!
`redis` обязателен!

Если предполагается запуск на локальной машине, то необходимо изменить `start_webhook` на `start_poling` см. > [пример](https://github.com/bbt-t/call-support/blob/master/start.py)

Необходмо создать файл с именем `.env`, прописать туда консанты (или просто явно указать значения в config.py):
```
HOST_REDIS = ...
BOT_TOKEN = ...
API_WEATHER = ...
и т.д
``` 
Для работы бота необходим python версии >= `3.10.x`

Для распознавания/синтеза речи `онлайн` и получение прогноза погоды необходимо использовать свои :key: API:
- [Yandex STT](https://cloud.yandex.ru/docs/speechkit/stt/)
- [Yandex TTS](https://cloud.yandex.ru/docs/speechkit/tts/)
- [Погода](https://openweathermap.org/api)
- [Погода (альтернатива)](https://developer.accuweather.com)

Для  распознавания речи `офлайн` > [модель VOSK](https://alphacephei.com/vosk/models) закинуть в корневую папку.

Для распознавания текста на фото необходимо [заглянуть сюда](https://github.com/bbt-t/what_is_there) и раскомментировать соответствующий [хендлер](https://github.com/bbt-t/bot-pet/blob/master/handlers/__init__.py)

>Остальные зависимости смотри в :fast_forward: [poetry.lock](https://github.com/bbt-t/bot-pet-project/blob/master/poetry.lock)


### Попробовать бота

можно тут:

```
@my_Yuuko_bot
```
