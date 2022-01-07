
[:russia: На русском](README.md)
### About

>Telegram bot based on aiogram v2.x asynchronous library 


<details>
 <summary>What a bot can do for today</summary>
<ul>
  <li>Notify about weather :heavy_check_mark:</li>
  <li>Remind me to do something :heavy_check_mark:</li>
  <li>Save passwords :heavy_check_mark:</li>
  <li>Which days are "good" for a haircut :heavy_check_mark:</li>
  <li>Get a horoscope :heavy_check_mark:</li>
</ul>
</details>


### Start
To start, you need to build a docker container and run:
```
docker build -t bot-pet .
docker run -p 8000:8000 --name bot bot-pet:latest 
```
Or without docker:
```
python start.py
```
### ATTENTION!
> redis is required!

> if you intend to run / install on a local machine, then you need to change "start_webhook" to "start_poling" loock this > [example](https://github.com/bbt-t/call-support/blob/master/start.py)

> For the bot to work, you need python version >= 3.10.x

> [DOWNLOAD VOSK model](https://alphacephei.com/vosk/models) for offline voice recognition.

> To recognize and synthesize speech 'online', to receive a weather forecast, you must use your :key: API-keys. 

> all required dependencies :fast_forward: [poetry.lock](https://github.com/bbt-t/bot-pet-project/blob/master/poetry.lock)

> It is necessary to create a file named .env, write the consants there (or just explicitly specify the values in config.py):
```
HOST_REDIS = ...
BOT_TOKEN = ...
API_WEATHER = ...
и т.д
``` 
