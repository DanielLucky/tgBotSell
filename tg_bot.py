import asyncio
import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from parse import start_parse_all_games, DOMAIN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
markdown = """
    *bold text*
    """


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    id_chat = open('id_chat.txt').read().split()

    if str(message.chat.id) in id_chat:
        start_id_chat = open('start_id_chat.txt').read().split()
        start_id_chat.append(str(message.chat.id))

        with open('start_id_chat.txt', 'w') as f:
            for id in set(start_id_chat):
                f.write(id + '\n')
        await bot.send_message(message.chat.id, 'Статус бота: Запущен')
    else:
        await bot.send_message(message.chat.id, 'Ваша группа не зарегистрирована')
        print('Попытка запустить бота в не зарегистрированной группе:', message.chat.id)


@dp.message_handler(commands=['stop'])
async def process_start_command(message: types.Message):
    id_chat = open('id_chat.txt').read().split()

    if str(message.chat.id) in id_chat:
        start_id_chat = open('start_id_chat.txt').read().split()
        if str(message.chat.id) in start_id_chat:
            start_id_chat.remove(str(message.chat.id))
        else:
            bot.send_message(message.chat.id, 'Бот уже остановлен в этой группе!')

        with open('start_id_chat.txt', 'w') as f:
            for id in set(start_id_chat):
                f.write(id + '\n')
        await bot.send_message(message.chat.id, 'Статус бота: остановлен')
    else:
        await bot.send_message(message.chat.id, 'Ваша группа не зарегистрирована')
        print('Попытка остановить бота в не зарегистрированной группе:', message.chat.id)



async def push_sell():
    while True:
        start_parse_all_games()
        start_id_chat = open('start_id_chat.txt').read().split()
        with open('old_target.json', 'r') as f:  # загружаем таргеты
            list_sell = json.load(f)

        for id_chat in start_id_chat: # проверка и выгрузка таргета распродажи в группы.
            for target in list_sell:

                push_groupe_id = list_sell[target]['push_groupe_id']

                if id_chat in push_groupe_id:
                    # print('Скидка в этой группе опубликована')
                    continue

                else:
                    add_groupe_id = [id_chat]
                    list_sell[target]['push_groupe_id'] = push_groupe_id + add_groupe_id
                    await bot.send_photo(id_chat, DOMAIN + list_sell[target]['details_image'],
                                                 list_sell[target]['details_list'] + '\n' +
                                                 list_sell[target]['details_buy'])
        with open('old_target.json', 'w') as f:
            json.dump(list_sell, f, indent=4, ensure_ascii=False)

        await asyncio.sleep(3600)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(push_sell())
    executor.start_polling(dp)

