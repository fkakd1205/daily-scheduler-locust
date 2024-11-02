from datetime import datetime, timedelta
import random

from locust import HttpUser, task, between, SequentialTaskSet

class SearchSchedulesForUsers(HttpUser):
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(1, 2)  # 스레드 시작 여유 시간 설정
        userId = -1
        today = datetime.now()
        endDate = datetime.strftime(datetime(today.year, today.month + 1, 1) - timedelta(days=1), "%Y.%m.%d 23:59:59")
        startDate = datetime.strftime(datetime(today.year, today.month, 1), "%Y.%m.%d 00:00:00")

        @task
        def sign_in(self):
            # 로그인
            self.userId = random.randint(0, 1000)
            self.client.post("/api/v1/users/sign-in", json={
                "userId": "test" + str(self.userId),
                "password": "test" + str(self.userId)
            })

        @task
        def seach_summary_for_users(self):
            self.client.get("/api/v1/schedules/summary", params={
                "startDate": self.startDate,
                "endDate": self.endDate
            })


