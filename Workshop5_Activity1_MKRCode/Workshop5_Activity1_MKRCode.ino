#include "Arduino_BHY2Host.h"
Sensor temp(SENSOR_ID_TEMP);
Sensor pressure(SENSOR_ID_BARO);
Sensor gas(SENSOR_ID_GAS);

void setup() { 
  Serial.begin(115200);
  BHY2Host.begin();
  temp.begin();
  pressure.begin();
  gas.begin();
}

void loop() {
  // If prompted, collect some data
  if (Serial.available()) {
    
    // Reads input in form of (number of readings, readings per second)
    // Find the number of readings to take
    String numberOfReadingsString = Serial.readStringUntil(',');
    int numberOfReadings = numberOfReadingsString.toInt();

    // Find the delay time in ms between readings
    String rateOfReadingsString = Serial.readStringUntil('\n');
    float rateOfReadings = rateOfReadingsString.toFloat();
    float delayTime = 1000.0/rateOfReadings;

    // Make a note of the time at which data taking start
    unsigned long startTime = millis();

    send_data(numberOfReadings, delayTime, startTime);
  } // ends if(Serial.available())
} // end loop()

void send_data(int n_readings, float d_time, float t0){
  // Initialise the time stamp variable
  float dataT = 0;

  for (int n = 0; n < n_readings; n++) {  
    // Update the sensor readings 
    BHY2Host.update();

    // Wait until it is time to take a new reading
    while ( dataT < (n*d_time) ) {
      delay(1);
      dataT = millis() - t0;
    }

    // Collect the data
    dataT = millis() - t0;
    float dataTemp = temp.value();
    float dataP = pressure.value();
    float dataG = gas.value();

    // Write the data to the serial port
    Serial.print(dataT);
    Serial.print(',');
    Serial.print(dataTemp);
    Serial.print(',');
    Serial.print(dataP);
    Serial.print(',');
    Serial.print(dataG);
    Serial.print('\n');
  } // ends for() loop
}
