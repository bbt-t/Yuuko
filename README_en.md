<p align="center">
  <img alt="" src="https://i.ibb.co/FX1jp6H/preview-logo.webp" width="500px">
</p>

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/bbt-t/Yuuko/blob/master/LICENSE)
[![Latest release](https://badgen.net/github/release/Naereen/Strapdown.js)](https://github.com/bbt-t/Yuuko/releases/tag/v2.7.5)
[![docker](https://badges.aleen42.com/src/docker.svg)](https://www.docker.com/get-started)
[![python](https://badges.aleen42.com/src/python.svg)](https://www.python.org/downloads/release/python-3102/)

[:russia: На русском](README.md)
### About

>Telegram bot based on aiogram v2.x asynchronous library, supports 2 languages [RU, EN]


<details>
 <summary>What a bot can do for today</summary>
<ul>
  <li>Notify about weather :heavy_check_mark:</li>
  <li>Remind me to do something :heavy_check_mark:</li>
  <li>Save passwords :heavy_check_mark:</li>
  <li>Which days are "good" for a haircut :heavy_check_mark:</li>
  <li>Get a horoscope :heavy_check_mark:</li>
  <li>Recognize text on photo ️:warning:</li>
  <li>Save recipes :heavy_check_mark:</li>
</ul>
</details>

***

### Start
To start, you need to build a `docker` container and run:

    docker build -t Yuuko_bot .
    docker run -p 8000:8000 --name bot Yuuko_bot:latest 

Or without docker:

    python start.py

_see more with_ `--help` _command_

***

### ATTENTION!
`redis` <s>is required!</s> (NO!)

If you plan to run a bot with `polling` in docker, then you need to change the value in `ENTRYPOINT` "webhook" to "polling" or remove it altogether


It is necessary to create a file named .env, write the consants there (or just explicitly specify the values in config.py)

[> Example .env <](https://github.com/bbt-t/Yuuko/blob/master/.example_env.md)

 
For the bot to work, you need python version >= `3.10.x`

To recognize and synthesize voice `online`, to receive a weather forecast, you must use your :key: API-keys:
- [Yandex STT](https://cloud.yandex.ru/docs/speechkit/stt/)
- [Yandex TTS](https://cloud.yandex.ru/docs/speechkit/tts/)
- [Weather](https://openweathermap.org/api)
- [Weather (alternative)](https://developer.accuweather.com)

[DOWNLOAD VOSK model](https://alphacephei.com/vosk/models) for `offline` voice recognition (put in the root folder).

For text recognition on a photo, you need to [look here](https://github.com/bbt-t/what_is_there) and uncomment the corresponding [handler](https://github.com/bbt-t/bot-pet/blob/master/handlers/__init__.py)

> all required dependencies :fast_forward: [poetry.lock](https://github.com/bbt-t/bot-pet-project/blob/master/poetry.lock)

***

### Try in action

__incomplete translation from Russian lang (work in progress)__

👉 `@my_Yuuko_bot`
