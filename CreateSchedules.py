from locust import HttpUser, task, between, SequentialTaskSet
import random

"""
랜덤한 유저가 스케쥴을 다중 생성하는 테스트 
"""
class CreateSchedules(HttpUser):
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(1, 2)  # 스레드 시작 여유 시간 설정
        categories_id = []
        userId = -1

        @task
        def search_category(self):
            # 카테고리 조회
            categories = self.client.get("/api/v1/schedule-categories/all").json()['data']
            for category in categories:
                self.categories_id.append(category['id'])

        @task
        def sign_in(self):
            # 로그인
            self.userId = random.randint(0, 1000)
            self.client.post("/api/v1/users/sign-in", json={
                "userId": "test" + str(self.userId),
                "password": "test" + str(self.userId)
            })

        @task
        def create_schedule(self):
            self.client.post("/api/v1/schedules", json={
                "content": "테스트 스케쥴" + str(random.randint(1, 100000)),
                "categoryId": self.categories_id[random.randint(0, len(self.categories_id) - 1)]
            })
