<p align="center">
  <img alt="" src="https://i.ibb.co/FX1jp6H/preview-logo.webp" width="500px">
</p>

[:us: English version](README_en.md)
### О боте

>Телеграм бот на основе асинхронной библиотеки aiogram v2.x


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
Собрать docker-контейнер и запустить:
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
> redis обязателен!

> если предполагается запуск на локальной машине, то необходимо изменить "start_webhook" на "start_poling" см. > [пример](https://github.com/bbt-t/call-support/blob/master/start.py)

> Для работы бота необходим python версии >= 3.10.x

> [СКАЧАТЬ модель VOSK](https://alphacephei.com/vosk/models) для офлайн распознавания голоса.

> Для распознавания и синтеза речи 'онлайн', получение прогноза погоды необходимо использовать свои :key: API.

> Остальные зависимости смотри в :fast_forward: [poetry.lock](https://github.com/bbt-t/bot-pet-project/blob/master/poetry.lock)

> Необходмо создать файл с именем .env, пописать туда консанты (или просто явно указать значения в config.py):
```
HOST_REDIS = ...
BOT_TOKEN = ...
API_WEATHER = ...
и т.д
``` 
> Для распознавания текста необходимо  [заглянуть сюда](https://github.com/bbt-t/what_is_there) и раскомментировать соответствующий [хендлер](https://github.com/bbt-t/bot-pet/blob/master/handlers/__init__.py)

### Попробовать бота
можно тут:
```
@simple_brain_bot
```
