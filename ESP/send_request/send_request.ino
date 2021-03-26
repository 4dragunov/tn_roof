#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include "HX711.h"                                            // подключаем библиотеку для работы с тензодатчиком
#define DOUT_PIN 5
#define SCK_PIN 4
HX711 scale;
float calibration_factor = -20.7;  // вводим калибровочный коэффициент
float data;
const char* ssid = "Keenetic-6399"; //Enter SSID
const char* password = "DxHGLBwT"; //Enter Password
String serverName = "http://127.0.0.1:8000";
float last_value = 0;

void setup() {
  scale.begin(DOUT_PIN, SCK_PIN);                             // инициируем работу с датчиком
  scale.set_scale();                                          // выполняем измерение значения без калибровочного коэффициента
  scale.tare();                                               // сбрасываем значения веса на датчике в 0
  scale.set_scale(calibration_factor);                        // устанавливаем калибровочный коэффициент

  Serial.begin(115200);          //Serial connection
  WiFi.begin(ssid, password);   //WiFi connection

  while (WiFi.status() != WL_CONNECTED) {  //Wait for the WiFI connection completion

    delay(500);
    Serial.println("Waiting for connection");

  
  }

}

void loop() {
  data = scale.get_units(20) + last_value;
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject();

//     JSONencoder["building"] = "Pentagon";
    JSONencoder["sensor_uid"] = "x000001";
    JSONencoder["value"] = data;
    JSONencoder["zero_data"] = 500;
    JSONencoder["is_debug"] = 1;


    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    Serial.println(JSONmessageBuffer);

    HTTPClient http;    //Declare object of class HTTPClient

    http.begin("http://178.154.201.111/api/v1/send/");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header

    int httpCode = http.POST(JSONmessageBuffer);   //Send the request

    Serial.println(httpCode);   //Print HTTP return code
    if (httpCode > 0) {
      
      // Parsing
      const size_t bufferSize = 400;
      DynamicJsonBuffer jsonBuffer(bufferSize);
      JsonObject& root = jsonBuffer.parseObject(http.getString());
      
      const char* message = root["message"];
      float last_value = root["last_value"];
      Serial.print("message:");
      Serial.print(message);
      Serial.print("last_value:");
      Serial.print(last_value);

      if (last_value > 0) {
        data = data + last_value;
      }
      
      
      
      
      
      }

    http.end();  //Close connection

  } else {

    Serial.println("Error in WiFi connection");

  }

  delay(5000);  //Send a request every 30 seconds

}
