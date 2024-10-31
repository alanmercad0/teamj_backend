from locust import HttpUser, task, between

URL = "http://127.0.0.1:5000"

INDEX = f"{URL}/"
GET_USERS = f"{URL}/users"
SIGNUP = f"{URL}/signup"
LOGIN = f"{URL}/login"
PROCESS_SONG = f"{URL}/process_song"


class LoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    @task
    def query_db(self):
        self.client.get(URL)  # Replace with your Flask route
        self.client.get(GET_USERS)
        

# Run with: locust -f users_tester.py