#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "esp_camera.h"
#include <WebSocketsClient.h>

// Настройки подключения к Wi-Fi
const char* ssid = "Redmi Note 13";
const char* password = "98765432";

// Настройки для WebSocket-соединения с сервером
const char* websocket_server_ip = "192.168.245.95";  // IP-адрес вашего Django сервера
const uint16_t websocket_server_port = 8000;  // Порт, на котором работает сервер
const char* websocket_url = "/ws/video/";  // Путь к WebSocket на сервере

WebSocketsClient webSocket;

// Настройка камеры
void startCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sccb_sda = 26;
  config.pin_sccb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_CIF;  // Можно изменить на другое разрешение
  config.jpeg_quality = 10;            // Качество JPEG
  config.fb_count = 2;

  pinMode(32, OUTPUT);
  digitalWrite(32, LOW);

  // Инициализируем камеру
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    return;
  }
}

// Отправляем кадр на сервер через WebSocket
void sendCameraFrame() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  if (fb->len > 0) {
    webSocket.sendBIN(fb->buf, fb->len);
    Serial.printf("Sent frame: %d bytes\n", fb->len);
  } else {
    Serial.println("Empty frame captured");
  }

  esp_camera_fb_return(fb);  // Освобождаем буфер
}

// Подключение к WebSocket серверу
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("Disconnected from server. Reconnecting...");
      webSocket.begin(websocket_server_ip, websocket_server_port, websocket_url);
      break;
    case WStype_CONNECTED:
      Serial.println("Connected to server");
      break;
    case WStype_BIN:
      Serial.println("Received binary data");
      break;
    default:
      break;
  }
}

void setup() {
  Serial.begin(115200);

  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("IP:");
  Serial.println(WiFi.localIP());
  // Инициализируем камеру
  startCamera();

  // Подключение к WebSocket
  webSocket.begin(websocket_server_ip, websocket_server_port, websocket_url);
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();

  // Периодическая отправка кадров
  static unsigned long lastFrameTime = 0;  // Переменная для отслеживания времени
  const unsigned long frameInterval = 100; // Интервал между кадрами (мс)

  unsigned long currentTime = millis();
  if (currentTime - lastFrameTime >= frameInterval) {
    lastFrameTime = currentTime;
    sendCameraFrame();  // Отправляем кадр
  }
}