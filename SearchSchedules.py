from datetime import datetime, timedelta

from locust import HttpUser, task, between

"""
한 유저가 스케쥴 요약 데이터를 지속적으로 요청하는 테스트
"""
class SearchSchedules(HttpUser):
    wait_time = between(1, 2)  # 스레드 시작 여유 시간 설정
    today = datetime.now()
    startDate = datetime.strftime(datetime(today.year, today.month, 1),"%Y.%m.%d 00:00:00")
    endDate = datetime.strftime(datetime(today.year, today.month+1, 1) - timedelta(days=1), "%Y.%m.%d 23:59:59")

    def on_start(self):
        # 로그인
        self.client.post("/api/v1/users/sign-in", json={
            "userId": "test456",
            "password": "123"
        })

    @task
    def search_summary(self):
        self.client.get("/api/v1/schedules/summary", params={
            "startDate": self.startDate,
            "endDate": self.endDate
        })
