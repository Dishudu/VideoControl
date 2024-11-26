from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

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