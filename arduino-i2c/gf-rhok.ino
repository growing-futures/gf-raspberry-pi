#include <Wire.h>

int ADXLAddress = 0x8; // Device address in which is also included the 8th bit for selecting the mode, read in this case.

void setup() {
  Serial.begin(9600);
  
  Wire.begin(ADXLAddress);      // join i2c bus with address #8
  Wire.onReceive(requestEvent); // register event
}

void loop() {
  delay(100);
}

void requestEvent(int byteCount) {
  //Serial.println(byteCount);

  /*
    I2C Commands:

      1:  Water Level
      2:  Air Humidity
      3:  Air Temperature
      4:  Water Temperature
      5:  pH
      6:  Light Status (1,2,3,4)

  */
Wire.write("test");
  switch (Wire.read()) {
    case 1:
      // Water Level
      Serial.println("Water Level");
      Wire.write(getWaterLevel());
      break;

      case 2:
      // Air Humidity
      Serial.println("Air Humidity");
      Wire.write(getAirHumidity());
      break;

      case 3:
      // Air Temperature
      Serial.println("Air Temperature");
      Wire.write(getAirTemperature());
      break;

      case 4:
      // Water Temperature
      Serial.println("Water Temperature");
      Wire.write(getWaterTemperature());
      break;

      case 5:
      // pH
      Serial.println("pH");
      Wire.write(getPH());
      break;

      case 6:
      // Light Status
      Serial.println("Light Status");
      //Wire.write(getLightStatus());
      break;
  }
  Serial.println("Sending on i2c");
}

int getWaterLevel() {
  return 100;
}

int getAirHumidity() {
  return 50;
}
int getAirTemperature() {
  return 25;
}

int getWaterTemperature() {
  return 12;
}

int getPH() {
  return 6;
}

String getLightStatus() {
  return "1,0,1,1";
}




