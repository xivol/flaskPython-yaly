import logging
import geo
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


@app.route('/alice', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)

    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new'] or req['request']['command'] == 'помощь':
        res['response']['text'] = \
            'Привет! Я могу найти страну по городу или сказать расстояние между городами!'
        return

    cities = get_cities(req)
    if not cities:
        res['response']['text'] = 'Ты не написал название ни одного города!'
    elif len(cities) == 1:
        res['response']['text'] = 'Этот город в стране - ' + \
                                  geo.get_country(cities[0])
    elif len(cities) == 2:
        city1 = geo.get_coordinates(cities[0])
        city2 = geo.get_coordinates(cities[1])
        distance = geo.get_distance(city1, city2)
        res['response']['text'] = 'Расстояние между этими городами: ' + \
                                  str(round(distance)) + ' км.'
    else:
        res['response']['text'] = 'Слишком много городов!'


if __name__ == '__main__':
    app.run()
