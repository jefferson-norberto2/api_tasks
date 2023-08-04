import requests

def get_tasks(user_id):
    url = 'http://localhost:5000/get_tasks'

    response = requests.post(url, data=str(user_id))
    
    if response.status_code == 200:
        return "OK"
    else:
        print(f"Error: {response.status_code}")
        return []

def send_task(task_data):
    url = 'http://localhost:5000/add_task'
    
    response = requests.post(url, json=task_data)
    
    if response.status_code == 200:
        result = response.json()
        return result['success']
    else:
        print(f"Error: {response.status_code}")
        return False

if __name__ == '__main__':
    user_id = 1  # Troque pelo ID do usuário desejado
    tasks = get_tasks(user_id)
    print(tasks)
