#include <WiFiClientSecure.h> 
#include <PubSubClient.h>

// Update these with values suitable for your network.
const char* ssid = "SP";
const char* password = "09032013";
const char* mqtt_server = "7ec23135bbf94e7599fa8e9a5a7ec748.s2.eu.hivemq.cloud";

const char* mqttUsername = "tuanvp34_device";
const char* mqttPassword = "Tuan3402";

#define RELAY 13
#define LEDPIN 15

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {
  delay(1000);
  Serial.begin(115200);
  espClient.setInsecure();
  wifiSetup();
  client.setServer(mqtt_server, 8883);
  client.setCallback(callback);
  //thêm setup thiết bị
  // Thiết lập chân relay
  pinMode(RELAY, OUTPUT);
  digitalWrite(RELAY, LOW);  // Kích thích relay để giữ trạng thái đóng
  // In trạng thái ban đầu của relay
  Serial.println("Trạng thái ban đầu của relay: " + String(digitalRead(RELAY)));
  
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);  // Tắt đèn ban đầu
}

void wifiSetup() {
  WiFi.begin(ssid, password);
  Serial.print("Connect to WiFi ..");
  while (!WiFi.isConnected()) {
    Serial.print(".");
    delay(1000);
  }
  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  String clientId = "";
  Serial.print("Connect to server..");
  while (!client.connected()) {
    Serial.print(".");
    if (client.connect(clientId.c_str(), mqttUsername, mqttPassword)) {
      Serial.println("\nConnect to server successful!");
      client.subscribe("test");
    } else{
      Serial.println("Connection failed. Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void callback(char* charArrTopic, byte* payload, unsigned int lenght) {
  String message;
  String topic = String(charArrTopic);
  for (int i = 0; i < lenght; i++)
    message += (char)payload[i];
  if(topic == "test"){
    if(message == "UnLock"){
      Serial.println("Received message from 'test' topic: " + message);
      unlock();
    }
    if(message == "Lock"){
      Serial.println("Received message from 'test' topic: " + message);
      lock();
    }
  }
}

void unlock() {
  digitalWrite(RELAY, HIGH);  // Kích thích relay (mở khóa)
  digitalWrite(LEDPIN, LOW);
  Serial.println("Unlocking...");
}

void lock() {
  digitalWrite(RELAY, LOW);  // Tắt relay (khóa)
  digitalWrite(LEDPIN, HIGH);
  Serial.println("Locking...");
}

void loop(){
  if(!client.connected()) {
      reconnect();
  }
  client.loop();
  //thêm hàm xử lý
}
