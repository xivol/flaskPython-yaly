import requests


def test_api(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Correct response:", resp.json())
    else:
        print(resp.status_code, resp.text)


# test_api("http://localhost:8080/api/jobs")
#
# test_api("http://localhost:8080/api/jobs/2")
#
# test_api("http://localhost:8080/api/jobs/14")
#
# test_api("http://localhost:8080/api/jobs/qwe")
#
# print(requests.post("http://localhost:8080/api/jobs",
#                     json={
#                         "job": "New job",
#                         "work_size": 23,
#                         "collaborators": "1",
#                         "is_finished": True,
#                         "team_leader": 1
#                     }).json())

test_api("http://localhost:8080/api/v2/users")

response = requests.post("http://localhost:8080/api/v2/users",
                         json={
                             "name": "Ilya",
                             "surname": "Loshkarev",
                             "age": 95,
                             "position": "Loshkarev",
                             "address": "Loshkarev",
                             "speciality": "Loshkarev",
                             "email": "loshkarev@yandexlyceum.ru",
                             "password": "1234",
                         })
print(response.json())

id = 1
response = requests.delete('http://localhost:8080/api/v2/users/' + str(id))
print(response.status_code, response.content)

test_api('http://localhost:8080/api/v2/users')

