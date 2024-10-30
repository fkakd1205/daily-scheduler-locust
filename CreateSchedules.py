from locust import HttpUser, task, between
import random

class CreateSchedulers(HttpUser):
    wait_time = between(1, 2)     # 스레드 시작 여유 시간 설정
    categories_id = []

    def on_start(self):
        # 로그인
        self.client.post("/api/v1/users/sign-in", json={
            "userId": "test456",
            "password": "123"
        })

        # 카테고리 조회
        categories = self.client.get("/api/v1/schedule-categories/all").json()['data']
        for category in categories:
            self.categories_id.append(category['id'])

    @task
    def create_schedule(self):
        self.client.post("/api/v1/schedules", json={
            "content": "테스트 스케쥴" + str(random.randint(1, 100000)),
            "categoryId": self.categories_id[random.randint(0, len(self.categories_id)-1)]
        })