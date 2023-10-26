from flask import Flask, request
from flask_socketio import SocketIO, emit
from scripts.scripts_sql import *
from cv2 import VideoCapture, imencode
from threading import Thread
from time import sleep
from base64 import b64encode
class WebSocketApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.socketio = SocketIO(self.app, cors_allowed_origins='*', async_mode=None)

         # Inicialize a câmera (substitua '0' pelo índice da sua câmera, se necessário)
        self.camera = VideoCapture(0)
        self.play = True

        # Set up WebSocket event handlers
        self.set_up_socket_events()

    def send_camera_frames(self):
        print('Starting camera thread...')
        while True:
            ret, self.frame = self.camera.read()
            if not ret:
                break

            # Convertendo o frame em JPEG e codificando-o como String
            _, buffer = imencode('.jpg', self.frame)
            jpg_as_text = b64encode(buffer).decode('utf-8')

            # Enviando o frame para todos os clientes conectados
            self.socketio.emit('camera_frame', {'image': jpg_as_text}, namespace='/camera')

            # Aguardar um pequeno intervalo entre o envio de cada frame
            sleep(0.016)


    def set_up_socket_events(self):
        self.socketio.on_event('sign_up_user', self.sign_up_user, namespace='/user')
        self.socketio.on_event('subscribe_camera', self.subscribe_camera, namespace='/camera')
    
    def subscribe_camera(self, data):
        print('Client subscribed to camera frames:', request.sid)
        if self.play:
            self.play = False
            self.send_camera_frames()

    
    def sign_up_user(self, message):
        print('User signed up', message)
        emit('user', True)

    def run(self):
        self.socketio.run(self.app, debug=True, host='127.0.0.1', port=10100)
    
    def on_connect(self):
        print('User connected')
        self.play = True
    
    def on_disconnect(self):
        print('User disconnected')
        self.play = False

if __name__ == '__main__':
    app = WebSocketApp()
    app.run()