# импортируем библиотеки
import werkzeug
from flask import Flask, request, jsonify
import logging

from werkzeug.exceptions import InternalServerError, BadRequest, abort

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}


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
    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    # Преобразовываем в JSON и возвращаем
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['card'] = {"type": "BigImage",
                                   "image_id": "1656841/9b44da685ffd3356e57e",
                                   "title": "Заголовок для изображения",
                                   "description": "Описание изображения.",
                                   "button": {
                                       "text": "Надпись на кнопке",
                                       "url": "http://example.com/",
                                       "payload": {}
                                   }
                                   }
        res['response']['end_session'] = True
        return


    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
