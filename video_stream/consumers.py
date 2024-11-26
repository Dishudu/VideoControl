import cv2
import numpy as np
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connected to ESP32-CAM")
    
    async def disconnect(self, close_code):
        print("Disconnected")
    
    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # nparr = np.frombuffer(bytes_data, np.uint8)
            # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # cv2.imwrite('frame.jpg', frame)
            # Отправляем клиенту бинарные данные кадра
            await self.channel_layer.group_send(
                "video_stream",
                {
                    "type": "send_frame",
                    "frame": bytes_data,
                }
            )

class BrowserVideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Добавление браузера в группу потоков
        await self.channel_layer.group_add("video_stream", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("video_stream", self.channel_name)

    async def send_frame(self, event):
        frame = event['frame']
        # Отправляем кадры браузеру
        await self.send(bytes_data=frame)