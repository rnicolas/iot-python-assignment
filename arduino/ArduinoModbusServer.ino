/*
  WiFi Modbus TCP Server LED

  This sketch creates a Modbus TCP Server with a simulated coil.
  The value of the simulated coil is set on the LED

  Circuit:
   - MKR1000 or MKR WiFi 1010 board

  created 16 July 2018
  by Sandeep Mistry
*/

#include <WiFi101.h> // for MKR1000
#include <ArduinoModbus.h>
#include "arduino_secrets.h"

int status = WL_IDLE_STATUS;

WiFiServer wifiServer(502);

ModbusTCPServer modbusTCPServer;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Power-Elec 6 emulator");

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(SECRET_SSID);
    // Connect to WPA/WPA2 network.
    status = WiFi.begin(SECRET_SSID, SECRET_PASS);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the status:
    printWifiStatus();

  // start the server
  wifiServer.begin();

  // start the Modbus TCP server
  if (!modbusTCPServer.begin()) {
    Serial.println("Failed to start Modbus TCP Server!");
    while (1);
  }

  // configure input registers
  configureModbusTCPServer();
}

void loop() {
  // update registers with new information
  updateModbusRegisters();

  // listen for incoming clients
  WiFiClient client = wifiServer.available();
  if (client) {
    // a new client connected
    Serial.println("new client");

    // let the Modbus TCP accept the connection 
    modbusTCPServer.accept(client);

    while (client.connected()) {
      // poll for Modbus TCP requests, while client connected
      modbusTCPServer.poll();
      updateModbusRegisters();
    }

    Serial.println("client disconnected");
  }
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void configureModbusTCPServer() {
  modbusTCPServer.configureInputRegisters(0, 460);
  modbusTCPServer.inputRegisterWrite(0, 0x0106);
  modbusTCPServer.inputRegisterWrite(1, 0x0002);
  modbusTCPServer.inputRegisterWrite(2, 0xf8f0); //MAC Address
  modbusTCPServer.inputRegisterWrite(3, 0x05ec); //MAC Address
  modbusTCPServer.inputRegisterWrite(4, 0x93ba); //MAC Address

  // initialize remaining registers to 0
  for (uint16_t i = 5; i < 460; i++) {
    modbusTCPServer.inputRegisterWrite(i, 0x0000);
  }
}

void updateModbusRegisters() {
  updateActiveEnergyImportIndex();
  updateReactiveEnergyImportIndex();
  updateActiveEnergyExportIndex();
  updateReactiveEnergyExportIndex();
  updateActivePower();
  updateReactivePower();
  updatePowerFactor();
  updateRMSCurrent();
  updateRMSCurrentAverage();
  updateRMSVoltage();
  updateRMSVoltageAverage();
  updateFrequency();
}

void updateRegisters(uint16_t start, uint8_t wpc, float newValue) {
  for (uint8_t connector = 1; connector <= 6; connector++) {
    for (uint8_t channel = 1; channel <= 3; channel++) {
      uint16_t reg = start + ((connector-1)*3 + channel-1) * wpc;
      uint16_t ui8ModbusRegister[2];
      memcpy(ui8ModbusRegister, &newValue, sizeof(float));
      modbusTCPServer.inputRegisterWrite(reg, ui8ModbusRegister[0]);
      modbusTCPServer.inputRegisterWrite(reg+1, ui8ModbusRegister[1]);
    }
  }
}

void updateActiveEnergyImportIndex(){
  updateRegisters(28, 2, getRandomNumberInRange(160, 170));
}
void updateReactiveEnergyImportIndex(){
  updateRegisters(64, 2, getRandomNumberInRange(160, 165));
}
void updateActiveEnergyExportIndex(){
  updateRegisters(100, 2, getRandomNumberInRange(0, 1));
}
void updateReactiveEnergyExportIndex(){
  updateRegisters(136, 2, getRandomNumberInRange(0, 1));
}
void updateActivePower(){
  updateRegisters(172, 2, getRandomNumberInRange(183, 186));
}
void updateReactivePower(){
  updateRegisters(208, 2, getRandomNumberInRange(227, 230));
}
void updatePowerFactor(){
  updateRegisters(244, 2, getRandomNumberInRange(1, 1));
}
void updateRMSCurrent(){
  updateRegisters(280, 2, getRandomNumberInRange(0, 7000));
}
void updateRMSCurrentAverage(){
  updateRegisters(316, 2, getRandomNumberInRange(0, 7000));
}
void updateRMSVoltage(){
  updateRegisters(352, 2, getRandomNumberInRange(100, 240));
}
void updateRMSVoltageAverage(){
  updateRegisters(388, 2, getRandomNumberInRange(100, 240));
}
void updateFrequency(){
  updateRegisters(424, 2, getRandomNumberInRange(50, 60));
}

float getRandomNumberInRange(int rangeStart, int rangeEnd){
  float number = random(rangeStart*10, (rangeEnd*10)+1)/10.0;
  return number;
}