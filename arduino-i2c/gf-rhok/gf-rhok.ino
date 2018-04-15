#include <Wire.h>

int ADXLAddress = 0x8; // Device address in which is also included the 8th bit for selecting the mode, read in this case.
int CMD = 0;

void setup() {
  Serial.begin(9600);
  
  Wire.begin(ADXLAddress);      // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
  Wire.onReceive(receiveEvent);
}

void loop() {
}

void receiveEvent(int byteCount){
  if(Wire.available() > 0)
  {
     CMD = Wire.read();
  }
}

void requestEvent() {
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
  switch (CMD) {
    case 1:
      // Water Level
      //Serial.println("Water Level");
      Wire.write(getWaterLevel().c_str());
      break;

      case 2:
      // Air Humidity
      //Serial.println("Air Humidity");
      Wire.write(getAirHumidity().c_str());
      break;

      case 3:
      // Air Temperature
      //Serial.println("Air Temperature");
      Wire.write(getAirTemperature().c_str());
      break;

      case 4:
      // Water Temperature
      //Serial.println("Water Temperature");
      Wire.write(getWaterTemperature().c_str());
      break;

      case 5:
      // pH
      //Serial.println("pH");
      //Wire.write("6.5");
      
      Wire.write(getPH().c_str());
      break;

      case 6:
      // Light Status
      //Serial.println("Light Status");
      Wire.write(getLightStatus().c_str());
      break;
  }

  //Wire.write("abc");
  //Serial.println("Sending on i2c");
}

String getWaterLevel() {
  return "100";
}

String getAirHumidity() {
  return "50";
}
String getAirTemperature() {
  return "25";
}

String getWaterTemperature() {
  return "12";
}

String getPH() {
  //delay(1000);
  return "6.5";
}

String getLightStatus() {
  return "1,0,1,1";
}
