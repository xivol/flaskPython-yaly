import requests

def test_jobs_api(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Correct response:", resp.json())
    else:
        print(resp.status_code, resp.text)


test_jobs_api("http://localhost:8080/api/jobs")

test_jobs_api("http://localhost:8080/api/jobs/2")

test_jobs_api("http://localhost:8080/api/jobs/14")

test_jobs_api("http://localhost:8080/api/jobs/qwe")

print(requests.post("http://localhost:8080/api/jobs",
                    json={
                        "job": "New job",
                        "work_size": 23,
                        "collaborators": "1",
                        "is_finished": True,
                        "team_leader": 1
                    }).json())

