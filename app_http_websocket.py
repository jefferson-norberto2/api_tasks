from flask_socketio import SocketIO
from flask import Flask, request
from scripts.scripts_sql import *
from database import Database
import protobuf.user.user as proto_user
import protobuf.tasks.tasks as proto_tasks
from eventlet import listen, wsgi


# Create a Flask application
class AppApi:
    def __init__(self):
        self._app = Flask(__name__)
        self._app.config['SECRET_KEY'] = 'secret'
        self._app.config['SESSION_TYPE'] = 'filesystem'
        self.socketio = SocketIO(self._app, cors_allowed_origins='*', async_mode=None)
        self._user = proto_user.User
        self._task = proto_tasks.Task
        self._list_tasks = proto_tasks.Tasks
        self.total_tasks = 0
    
        # Register routes
        self.register_routes()

        # Set up WebSocket event handlers
        self.set_up_socket_events()

        # Create the database tables
        self.create_tables()
    
    def register_routes(self):
        self._app.add_url_rule('/sign_up_user', 'sign_up_user', self.sign_up_user, methods=['POST'])
        self._app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self._app.add_url_rule('/add_task', 'add_task', self.add_task, methods=['POST'])
        self._app.add_url_rule('/get_tasks', 'get_tasks', self.get_tasks, methods=['GET'])
    
    def set_up_socket_events(self):
        self.socketio.on_event('update_request', self.counter_tasks, namespace='/counter')
        self.socketio.on_event('disconnect', self.handle_disconnect)
    
    def create_tables(self):
        self._database = Database(DATABASE_PATH)
        self._database.execute_query(CREATE_USER_TABLE)
        self._database.execute_query(CREATE_TASK_TABLE)
        self._database.close_connection()
    
    def counter_tasks(self, message):
        id = int(message)
        database = Database(DATABASE_PATH)

        # Get the tasks data from the database
        query = f'''
            SELECT * FROM {TASK_TABLE_NAME}
            WHERE {USER}={id}
        '''
        tasks = database.fetch_all(query)
        database.close_connection()

        self.total_tasks = len(tasks)

        # Return a response to the Flutter 
        self.socketio.emit('update_response', str(self.total_tasks), namespace='/counter')
    
    def sign_up_user(self):
        # Get user data from the request
        message = request.data
        obj_user =  self._user.FromString(message)

        database = Database(DATABASE_PATH)
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

        database.execute_query(query, values)
        database.close_connection()

        # Return a response to the Flutter application
        return {'user': True}
    
    def add_task(self):
        data = request.data
        task = self._task.FromString(data)

        database = Database(DATABASE_PATH)
        # Get pet data from the request
        
        query = f''' INSERT INTO {TASK_TABLE_NAME} (
                                {TASK},
                                {USER}
                                ) VALUES ( ?, ?)'''
        values = (task.task, task.user_id)

        # Insert the pet data into the database
        database.execute_query(query, values)

        self.total_tasks += 1

        self.socketio.emit('update_response', str(self.total_tasks), namespace='/counter')
        return {'task': True}
    
    def get_tasks(self):
        id = request.headers.get('id')
        id = int(id)    

        database = Database(DATABASE_PATH)

        # Get the tasks data from the database
        query = f'''
            SELECT * FROM {TASK_TABLE_NAME}
            WHERE {USER}={id}
        '''
        tasks = database.fetch_all(query)
        database.close_connection()

        # Create a list of tasks
        user_tasks = proto_tasks.Tasks()
        for task in tasks:
            task_send = proto_tasks.Task()
            task_send.id = str(task[0])
            task_send.task = task[1]
            task_send.user = str(task[2])
            user_tasks.tasks.append(task_send)
        # Return a response to the Flutter 
        return user_tasks.SerializeToString()
    
    def login(self):
        message = request.data
        obj_user =  self._user.FromString(message)

        database = Database(DATABASE_PATH)
        # # Get user data from the request
        name = obj_user.name
        password = obj_user.password

        query = f'''
            SELECT * FROM users
            WHERE {USER_NAME}=? AND {PASSWORD}=?
        '''
        values = (name, password)
        # Search for the user in the database
        user = database.fetch_one(query, values)

        database.close_connection()
        # Return a response to the Flutter application
        if user:
            user_send = proto_user.User()
            user_send.id = str(user[0])
            user_send.name = user[1]
            user_send.password = user[2]
            return user_send.SerializeToString()
        else:
            return 'User not found'
    
    def handle_disconnect(self):
        print("Client disconnected")
    
    def run(self):
        try:
            wsgi.server(listen(('127.0.0.1', 10100)), self._app)
        except Exception as e:
            print(e)
    
if __name__ == '__main__':
    app = AppApi()
    app.run()
