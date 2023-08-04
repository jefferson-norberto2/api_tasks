from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from database import Database
import protobuf.user.user as proto_user
import protobuf.tasks.tasks as proto_tasks
from scripts.scripts_sql import *

class WebSocketApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.socketio = SocketIO(self.app, cors_allowed_origins='*', async_mode=None)
        self._user = proto_user.User
        self._task = proto_tasks.Task
        self._user_tasks = proto_tasks.User

        # Register routes
        self.register_routes()

        # Set up WebSocket event handlers
        self.set_up_socket_events()

    def register_routes(self):
        self.app.route('/', methods=['GET', 'POST'])(self.index)

    
    def index(self):
        return jsonify({'data': "Web Socket Example"})

    def set_up_socket_events(self):
        self.socketio.on_event('sign_up_user', self.sign_up_user, namespace='/user')
        self.socketio.on_event('login', self.get_user, namespace='/user')
        self.socketio.on_event('get_tasks', self.get_tasks, namespace='/user')
        self.socketio.on_event('add_task', self.add_task, namespace='/user')
        self.socketio.on_event('event', self.event_handler, namespace='/user')

    def event_handler(self, message):
        print(message)
        emit('event', "Recebi")
    
    def sign_up_user(self, message):
        # Get user data from the request
        obj_user =  self._user.FromString(message)

        self._database = Database(DATABASE_PATH)
        full_name = obj_user.name
        password = obj_user.password

        print(full_name)
        print(password)
        
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
        emit('user', True)

    def get_user(self, message):
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
            emit('login', user_send.SerializeToString())
        else:
            emit('login', 'User not found')

    def add_task(self, message):
        task = self._task.FromString(message)

        self._database = Database(DATABASE_PATH)

        # Get pet data from the request
        query = f''' INSERT INTO {TASK_TABLE_NAME} (
                                {TASK},
                                {USER}
                                ) VALUES ( ?, ?)'''
        values = (task.task, task.user_id)

        # Insert the pet data into the database
        self._database.execute_query(query, values)
        self._database.close_connection()

        # Return a response to the Flutter application
        emit('add_task', True)
    
    def get_tasks(self, message):
        id = message
        id = int(id)

        self._database = Database(DATABASE_PATH)
        # Get the tasks data from the database
        tasks = self._database.fetch_all(f'''
            SELECT * FROM {TASK_TABLE_NAME}
            WHERE {USER}={id}
        ''')

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
        
        return user_tasks.SerializeToString()

    def run(self):
        self.socketio.run(self.app, debug=True, host='localhost', port=5001)
    
    def on_connect(self):
        print('User connected')

if __name__ == '__main__':
    app = WebSocketApp()
    app.run()