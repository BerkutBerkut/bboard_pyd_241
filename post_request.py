import requests

url = "http://127.0.0.1:8000/todo_create/"
data = {"title": "Test Task", "description": "This is a test task.", "completed": False}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
