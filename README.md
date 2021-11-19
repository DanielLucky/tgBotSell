# tgBotSell

tgBotSell - это телеграмм бот, рассылающий бесплатные предложения игр.

## Посмотреть

[*тык*](https://t.me/joinchat/IpUDlZtYS0dmZDVi)


## Функции 
- Парсинг страницы распродажи (https://freegames.codes/game/)
- Добавление скидки в json файл
- Рассылка группам

## Файлы
- tg_bot.py - телеграм бот
- parse.py - парсер страницы
- id_chat.txt - Список групп для рассылки (white list)
- start_id_chat.txt - список чатов в которые бот отправляет сообщения
- old_target.json - список активных скидок, содержит в себе инфрмацию о предложении и группы в которую предложение было отправлено

## Быстрый старт (unix)
- редактируем config.py - вставляем TOKEN полученный в [@BotFather](https://telegram.me/BotFather "BotFather")
- редактируем id_chat.txt - вставляем id чата
```sh
> git clone (скачать репозиторий) 
> pip install pipenv (установить pipenv, если не установлен)
> pipenv shell 
> python3 tg_bot.py
```

