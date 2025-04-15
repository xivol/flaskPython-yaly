# импортируем библиотеки
import random

import werkzeug
from flask import Flask, request, jsonify
import logging

from werkzeug.exceptions import InternalServerError, BadRequest, abort

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.DEBUG,
                    filename='log.log',
                    format="%(asctime)s %(message)s")
logging.getLogger("werkzeug").setLevel(logging.DEBUG)

sessionStorage = {}

cities= {
    'москва': ['1652229/f365b758cd8e2a9f91db',
               '1540737/e96a076bbb6986605131'],
    'нью-йорк': ['1652229/14904323a694ee5de67d',
                 '1521359/8458e7caf93aef3c3d21'],
    'париж': ["1521359/5392695d4de08901377b",
              '1652229/82619668d90c0c999a4c']
}

@app.errorhandler(BadRequest)
@app.errorhandler(InternalServerError)
def error(e):
    response = {
        'response': {
            'text': e.description,
            'end_session': True
        }
    }
    return jsonify(response)


@app.route('/alice', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON, который отправила нам Алиса в запросе POST
def main():
    logging.info('Request: %r', request.json)

    if 'session' not in request.json:
        return abort(400)

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog. Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(req=request.json, res=response)

    logging.info('Response: %r', request.json)

    # Преобразовываем в JSON и возвращаем
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['request']['command'] == 'помощь':
        res['response']['text'] = 'Назовите Алисе свое имя,\n и попытайтесь угадать какие города она знает!'
        return

    res['response']['buttons'] = [
        {
            'title': 'Помощь',
            'hide': True
        }
    ]




    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я - Алиса. Какой город хочешь увидеть?'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] += [
                {
                    'title': city.title(),
                    'hide': True
                } for city in cities
            ]
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе,
    # что хочет увидеть.
    else:
        # ищем город в сообщение от пользователя
        city = get_city(req)
        # если этот город среди известных нам,
        # то показываем его (выбираем одну из двух картинок случайно)
        if city in cities:
            res['response']['text'] = 'Я угадал!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю.'
            res['response']['card']['image_id'] = random.choice(cities[city])
            res['response']['card']['button']= {
                "text": "Надпись на кнопке",
                "url": "http://ya.ru?q="+city,
                "payload": {}
            }
        # если не нашел, то отвечает пользователю
        # 'Первый раз слышу об этом городе.'
        else:
            res['response']['text'] = \
                'Первый раз слышу об этом городе. Попробуй еще разок!'


def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO то пытаемся получить город(city),
        # если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)

if __name__ == '__main__':
    app.run()
