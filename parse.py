import json
import time

import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://freegames.codes'


def print_target(link):
    print(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    details_title = soup.find('div', class_='details__wrap').find('h1').text.strip()
    details_list = soup.find('div', class_='details__wrap').find('ul').text.strip()
    details_image = soup.find('div', class_='details__cover').find('img').get('src').strip()
    details_buy = soup.find('a', class_='details__buy').get('href').strip()

    return details_image, details_title, details_list, details_buy


def check_target(links):
    targets_querry = {}
    adds_target = []

    with open('old_target.json', 'r') as f:  # загружаем старые таргеты
        targets_old = json.load(f)

    with open('old_target.json', 'w') as f:

        for i in links:
            target = i.split('/')[4]
            if target in targets_old:
                print('Таргет уже в базе:', i)
                adds_target.append(target)

            else:
                details_image, details_title, details_list, details_buy = print_target(i)
                print('*** Таргет на публикацию ***', '\n' + i)
                print('- details_image:', details_image)
                print('- details_title:', details_title)
                print('- details_list:', details_list)
                print('- details_buy:', details_buy)
                print('*** конец информаци о таргете ***')

                targets_querry[target] = {
                        'details_image': details_image,
                        'details_title': details_title,
                        'details_list': details_list,
                        'details_buy': details_buy,
                        'push_groupe_id': []
                    }
                time.sleep(3)
        # print('adds_target:', adds_target)
        adds_target += list(targets_querry.keys())
        # print('targets_querry + list(targets_querry.keys()) :', adds_target)

        for target in targets_old:
            if target in adds_target:
                targets_querry[target] = targets_old[target]

        # targets_all = {**targets_old, **targets_querry}
        # print('targets_querry:', targets_querry)
        # print('type(targets_querry)', type(targets_querry))

        json.dump(targets_querry, f, indent=4, ensure_ascii=False)

    return targets_querry


def start_parse_all_games():
    r = requests.get('https://freegames.codes/game/')

    links = set()
    target_id = set()
    soup = BeautifulSoup(r.text, "lxml")

    for pos in soup.findAll('a', class_='card__cover'):
        target = pos.get('href')
        links.add('https://freegames.codes/game/' + target)
        target_id.add(target.split('/')[0])

    print('id на странице all_free_games:', target_id)
    print(links)

    return check_target(links)


if __name__ == "__main__":
    start_parse_all_games()