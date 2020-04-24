# locustfile.py
from locust import HttpLocust, TaskSet, task, between
import json
import random


class OverloadaAPI(TaskSet):
    @task(1)
    def load_api(self):
        # POST to login page with csrftoken
        payload = [
                        {
                            "todo": "Some data",
                            "todo_due_date": "2020-04-15",
                            "todo_status": "todo",
                            "user_id": "bgw254"
                        }
                    ]

        self.client.get(
            url= f'api/v2/todos_add/?items={payload}'
        )




class WebsiteUser(HttpLocust):
    task_set = OverloadaAPI
    wait_time = between(1, 3)