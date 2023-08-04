import time
from flask import Flask, request
from scripts.scripts_sql import *
from database import Database
import base64
import protobuf.user.user as proto_user
import protobuf.tasks.tasks as proto_tasks


# Create a Flask application
class AppApi:
    def __init__(self):
        self._app = Flask(__name__)
        self._database = None
        self._user = proto_user.User
        self._task = proto_tasks.Task
        self._user_tasks = proto_tasks.User
    
        # Register routes
        self.register_routes()

        # Create the database tables
        self.create_tables()
    
    def register_routes(self):
        self._app.add_url_rule('/sign_up_user', 'sign_up_user', self.sign_up_user, methods=['POST'])
        self._app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self._app.add_url_rule('/add_task', 'add_task', self.add_task, methods=['POST'])
        self._app.add_url_rule('/get_tasks', 'get_tasks', self.get_tasks, methods=['POST'])
        self._app.add_url_rule('/test_route', 'test_route', self.test_route, methods=['GET'])
    
    def create_tables(self):
        self._database = Database(DATABASE_PATH)
        self._database.execute_query(CREATE_USER_TABLE)
        self._database.execute_query(CREATE_TASK_TABLE)
        self._database.close_connection()

    def test_route(self):
        return {'test': 'Executou em thread separada'}
    
    def sign_up_user(self):
        # Get user data from the request
        message = request.data
        obj_user =  self._user.FromString(message)

        self._database = Database(DATABASE_PATH)
        full_name = obj_user.name
        password = obj_user.password
        
        # Insert the user data into the database
        query = f'''
            INSERT INTO {USER_TABLE_NAME} (
                {USER_NAME},
                {PASSWORD}
            ) VALUES ( ?, ?)
        '''
        values = (full_name, password)

        self._database.execute_query(query, values)
        self._database.close_connection()

        # Return a response to the Flutter application
        return {'user': True}
    
    def add_task(self):
        data = request.data
        task = self._task.FromString(data)

        self._database = Database(DATABASE_PATH)
        # Get pet data from the request
        

        query = f''' INSERT INTO {TASK_TABLE_NAME} (
                                {TASK},
                                {USER}
                                ) VALUES ( ?, ?)'''
        values = (task.task, task.user_id)

        # Insert the pet data into the database
        self._database.execute_query(query, values)

        # Return a response to the Flutter application
        return {'user': True}
    
    def get_tasks(self):
        print('Entrou')
        id = request.data
        id = int(id)

        self._database = Database(DATABASE_PATH)

        # Get the tasks data from the database
        query = f'''
            SELECT * FROM {TASK_TABLE_NAME}
            WHERE {USER}={id}
        '''
        tasks = self._database.fetch_all(query)
        self._database.close_connection()

        # Create a list of tasks
        user_tasks = proto_tasks.User()
        for task in tasks:
            task_send = proto_tasks.Task()
            task_send.id = str(task[0])
            task_send.task = task[1]
            task_send.user = str(task[2])
            user_tasks.tasks.append(task_send)
        # Return a response to the Flutter 
        print('Enviando tarefas')
        return user_tasks.SerializeToString()
    
    def login(self):
        message = request.data
        obj_user =  self._user.FromString(message)

        self._database = Database(DATABASE_PATH)
        # # Get user data from the request
        name = obj_user.name
        password = obj_user.password

        # Search for the user in the database
        user = self._database.fetch_one(f'''
            SELECT * FROM users
            WHERE {USER_NAME}=? AND {PASSWORD}=?
        ''', (name, password))

        self._database.close_connection()
        # Return a response to the Flutter application
        if user:
            user_send = proto_user.User()
            user_send.id = str(user[0])
            user_send.name = user[1]
            user_send.password = user[2]
            return user_send.SerializeToString()
        else:
            return 'User not found'
    
    def run(self):
        try:
            self._app.run(host='localhost', port=5000, debug=True)
        except Exception as e:
            print(e)

    @staticmethod
    def save_image_from_base64(image_data, save_path):
        # Decode the base64-encoded image string
        image_bytes = base64.b64decode(image_data)

        # Save the image file
        with open(save_path, "wb") as file:
            file.write(image_bytes)

        return save_path

    def __del__(self):
        if self._database:
            self._database.close_connection()
    
if __name__ == '__main__':
    app = AppApi()
    app.run()
