from locust import HttpUser, task, between

import random

"""
한 명의 유저가 스케쥴을 다중 생성하는 테스트 
"""
class SearchSchedules(HttpUser):
    wait_time = between(1, 2)  # 스레드 시작 여유 시간 설정
    categories_id = []

    def on_start(self):
        # 로그인
        self.client.post("/api/v1/users/sign-in", json={
            "userId": "test456",
            "password": "123"
        })

        categories = self.client.get("/api/v1/schedule-categories/all").json()['data']
        for category in categories:
            self.categories_id.append(category['id'])

    @task
    def create_schedule(self):
        self.client.post("/api/v1/schedules", json={
            "content": "테스트 스케쥴" + str(random.randint(1, 100000)),
            "categoryId": self.categories_id[random.randint(0, len(self.categories_id) - 1)]
        })

