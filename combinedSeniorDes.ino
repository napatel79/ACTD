#include <Adafruit_LittleFS.h>
#include <Adafruit_TinyUSB.h>
#include <bluefruit.h>
#include <InternalFileSystem.h>
#include "UUID.h"

using namespace Adafruit_LittleFS_Namespace;


#define IDSIZE 16

UUID uuid; //Global UUID object
char device_id[37]; //UUID transmit string
char received_id[37]; //UUID receive string
int loopCount = 0; //number of 4 byte chunks received

File file(InternalFS);
void setupfile(const char*);
void printfileguids(const char*);
void writeUUID(const char*, bool);


BLEClientUart clientUart; // bleuart client
BLEUart bleuart; // uart over ble

void setup() {
  Serial.begin(115200);
  uuid.seed(123456789, 987654321);
  uuid.generate();
  memcpy(&device_id, uuid.toCharArray(), 37);
  setupfile("deviceid");
  writeUUID("deviceid", true);

  setupfile("day-1");
  setupfile("day-2");
  setupfile("day-3");
  setupfile("day-4");
  setupfile("day-5");
  setupfile("day-6");
  setupfile("day-7");


  
  Bluefruit.begin();
  Bluefruit.setName("Bluefruit52 Central");
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);
  Bluefruit.setTxPower(4);

  Bluefruit.Periph.setConnectCallback(prph_connect_callback);
  Bluefruit.Central.setConnectCallback(cent_connect_callback);

  
  clientUart.begin();
  clientUart.setRxCallback(bleuart_central_rx_callback);

  
  Bluefruit.Scanner.setRxCallback(scan_callback);
  Bluefruit.Scanner.restartOnDisconnect(true);
  Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  Bluefruit.Scanner.useActiveScan(false);
  Bluefruit.Scanner.start(0);


  startAdv();
}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);
  Bluefruit.ScanResponse.addName();
  
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds  
}

void loop() {
  printfileguids("deviceid");
  printfileguids("day-1");
  printfileguids("day-2");
  printfileguids("day-3");
  printfileguids("day-4");
  printfileguids("day-5");
  printfileguids("day-6");
  printfileguids("day-7");
  delay(10000);
}

void setupfile(const char* filename) {
  file.open(filename, FILE_O_WRITE);
  if (file) {
    file.close();
    InternalFS.remove(filename);
  }
  file.close();
}

void writeUUID(const char* filename, bool selfID) {
  file.open(filename, FILE_O_WRITE);
  if (file) {
    if(selfID) {
      file.write(device_id, sizeof(device_id));
    }
    else {
      file.write(received_id, sizeof(received_id));
    }
    file.close();
  }
}

void printfileguids(const char* filename) {
  Serial.println(filename);
  file.open(filename, FILE_O_READ);
  if (file) {
    while (file.available()) {
      Serial.write(file.read());
    }
    file.close();
  }
}


/**
 * Callback invoked when scanner pick up an advertising data
 * @param report Structural advertising data
 */
void scan_callback(ble_gap_evt_adv_report_t* report)
{
  // Check if advertising contain BleUart service
  if ( Bluefruit.Scanner.checkReportForService(report, clientUart) )
  {
    // Connect to device with bleuart service in advertising
    Bluefruit.Central.connect(report);
  }else
  {      
    // For Softdevice v6: after received a report, scanner will be paused
    // We need to call Scanner resume() to continue scanning
    Bluefruit.Scanner.resume();
  }
}

void cent_connect_callback(uint16_t conn_handle)
{
  // Serial.println("Connected");


  // Serial.print("Discovering BLE Uart Service ... ");
  if ( clientUart.discover(conn_handle) )
  {
    clientUart.enableTXD();
  }else
  {
    // disconnect since we couldn't find bleuart service
    Bluefruit.disconnect(conn_handle);
  }  
}

void bleuart_central_rx_callback(BLEClientUart& uart_svc)
{
  //Serial.print("[RX]: ");
  char buf[32];
  int count = 0;
  while ( uart_svc.available() )
  {
    count = uart_svc.read(buf, 4);
    sprintf(&received_id[loopCount*4], "%s", buf);
  }
  
  loopCount++;

  if(loopCount == 9) {
    received_id[36] = '\n';
    writeUUID("day-1", false);
    loopCount = 0;
  }
  
}


void prph_connect_callback(uint16_t conn_handle)
{
  // Get the reference to current connection
  BLEConnection* connection = Bluefruit.Connection(conn_handle);

  char central_name[32] = { 0 };
  connection->getPeerName(central_name, sizeof(central_name));

  Serial.print("Connected to ");
  Serial.println(central_name);
  delay(2000); //wait for central to be ready to receive
  Serial.println("Sending UUID");
  for (unsigned i = 0; i < 9; i++) {
    bleuart.write(&device_id[i*4], 4 );
  }
  Serial.println("Sent UUID");
}
