from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
import cv2
from .mqtt import send_relay_command
import json

# def gen_frames():
#     # В данном примере используется локальная камера.
#     # Замените URL-адрес на поток с ESP32-CAM, если необходимо.
#     cap = cv2.VideoCapture(0)  # 0 для локальной камеры или URL для удаленной камеры
#     # cap = cv2.VideoCapture('http://<ESP32-CAM-IP>/video') 
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def video_feed(request):
#     return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_stream(request):
    return render(request, 'video_stream/home.html')

def relay_control(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        command = data.get('command')
        if command in ['ON', 'OFF']:
            send_relay_command(command)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)