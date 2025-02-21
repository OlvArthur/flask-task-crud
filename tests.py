import pytest
import requests

from models.task import Task 

BASE_URL = 'http://127.0.0.1:5000'

tasks: list[Task] = []

def test_create_task():
  new_task_data: Task = {
     "title": "New task",
     "description": "task for testing"
  }

  response_data = requests.post(f'{BASE_URL}/tasks', json=new_task_data)

  assert response_data.status_code == 200 

  response_data_json = response_data.json()

  assert 'id' in response_data_json
  assert 'message' in response_data_json

  tasks.append(response_data_json['id'])

def test_get_task():
  response = requests.get(f"{BASE_URL}/tasks")

  response_json = response.json()

  assert response.status_code == 200
  assert 'tasks' in response_json
  assert 'total_tasks' in response_json           



def test_get_one_task():
  task_id = tasks[0]
  

  response = requests.get(f"{BASE_URL}/tasks/{task_id}")

  assert response.status_code == 200

  response_json = response.json()

  assert 'id' in response_json
  assert response_json['id'] == task_id

def test_update_Task():
   task_id = tasks[0]
   payload = {
     'title': 'New Updated title',
     'description': 'task to update',
     'completed': True
   }

   response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)

   assert response.status_code == 200

   response_json = response.json()
   assert 'message' in response_json

   response = requests.get(f'{BASE_URL}/tasks/{task_id}')
   assert response.status_code == 200
   response_json = response.json()

   assert response_json['id'] == task_id
   assert response_json['title'] == payload['title'] 
   assert response_json['description'] == payload['description'] 
   assert response_json['completed'] == payload['completed'] 


def test_delete_task():
   task_id = tasks[0]

   response = requests.delete(f'{BASE_URL}/tasks/{task_id}')

   assert response.status_code == 200

   response = requests.get(f'{BASE_URL}/tasks/{task_id}')
   
   response_json = response.json()

   assert response.status_code == 404
   assert response_json['message'] == 'Not possible to find this activity'