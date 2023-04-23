#include <Adafruit_LittleFS.h>
#include <Adafruit_TinyUSB.h>
#include <bluefruit.h>
#include <InternalFileSystem.h>
#include "UUID.h"


using namespace Adafruit_LittleFS_Namespace;

UUID uuid; //Global UUID object
char device_id[37]; //UUID transmit string
char received_id[37]; //UUID receive string
int loopCount = 0; //number of 4 byte chunks received
bool centralReceived = false; //disconnection purposes
bool centralSent = false; //disconnection purposes
File file(InternalFS); //read and write files
uint16_t centConnection; //central connection for disconnection purposes
int mtx = 0; //simple mutex

void setupfile(const char*); //create empty files
void printfileguids(const char*); //
void writeUUID(const char*, bool); //write an ID to file

BLEClientUart clientUart; // bleuart client
BLEUart bleuart; // uart over ble

void setup() {
  centralReceived = false;
  centralSent = false;
  loopCount = 0;
  InternalFS.begin();
  InternalFS.format(); //reset file system (TODO: change this so it doesn't reset on power loss)
  Serial.begin(115200);
  uuid.seed(123456789, 987654321); //One seed pair for each device to make the UUID's different
  // uuid.seed(987654321, 123456789);
  // uuid.seed(98765432, 12345678);

  //create uuid, convert to string, and write to file "deviceid"
  uuid.generate();
  memcpy(&device_id, uuid.toCharArray(), 37);
  device_id[36] = '\0';
  setupfile("deviceid");
  writeUUID("deviceid", true); 


  //setup other files for received id's
  setupfile("day-1");
  setupfile("day-2");
  setupfile("day-3");
  setupfile("day-4");
  setupfile("day-5");
  setupfile("day-6");
  setupfile("day-7");



  Bluefruit.begin(1,1); //1 central, 1 peripheral
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);
  Bluefruit.setTxPower(4);


  //what happens when devices connect and disconnect
  Bluefruit.Periph.setConnectCallback(prph_connect_callback);
  Bluefruit.Central.setConnectCallback(cent_connect_callback);

  Bluefruit.Periph.setDisconnectCallback(prph_disconnect_callback);
  Bluefruit.Central.setDisconnectCallback(cent_disconnect_callback);



  //init uart protocols for cent and prph and what to do when data received
  bleuart.begin();
  bleuart.setRxCallback(bleuart_peripheral_rx_callback);
  clientUart.begin();
  clientUart.setRxCallback(bleuart_central_rx_callback);


  //central scan for peripheral devices
  Bluefruit.Scanner.setRxCallback(scan_callback);
  Bluefruit.Scanner.restartOnDisconnect(true);
  Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  Bluefruit.Scanner.useActiveScan(false);
  Bluefruit.Scanner.start(0);



  startAdv();
}

//peripheral advertise to central devices
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

//repeats forever
void loop() {
  delay(1000);
  // if data has been sent and received then disconnect
  if(centralReceived && centralSent) {
    Bluefruit.disconnect(centConnection);
  }

  //print out the files to serial
  printfileguids("deviceid");
  printfileguids("day-1");
  printfileguids("day-2");
  printfileguids("day-3");
  printfileguids("day-4");
  printfileguids("day-5");
  printfileguids("day-6");
  printfileguids("day-7");
}

void setupfile(const char* filename) {
  file.open(filename, FILE_O_READ);
  if (file) {
    file.close();
    InternalFS.remove(filename);
  }
  if(file.open(filename, FILE_O_WRITE)) {
    file.close();
  }
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

//loop through the files to check for dupes (TODO: fix this to work all the time)
//current issue guess: not properly reading multiple lines?
bool checkForDuplicates(const char* filename) {
  char buf[37];
  file.open(filename, FILE_O_READ);
  if(file) {
    while(file.available()) {
      file.read(buf,37);
      buf[36] = '\0';
      if(strcmp(buf, received_id) == 0) {
        return true;
      }
      else {
        return false;
      }
    }
  }
  return false;
}


void printfileguids(const char* filename) {
  char buf[37];
  Serial.println(filename);
  file.open(filename, FILE_O_READ);
  if (file) {
    while (file.available()) {
      file.read(buf, 37);
      buf[36] = '\0';
      Serial.println(buf);
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
  if (Bluefruit.Scanner.checkReportForService(report, clientUart) )
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
    centConnection = conn_handle;
    clientUart.enableTXD();

    //central send UUID
    for (unsigned i = 0; i < 9; i++) {
      clientUart.write(&device_id[i*4], 4 );
    }
    centralSent = true;

  }else
  {
    // disconnect since we couldn't find bleuart service
    Bluefruit.disconnect(conn_handle);
  }

}

void bleuart_central_rx_callback(BLEClientUart& uart_svc)
{
  char buf[32]; //this can realistically be 4 bytes
  int count = 0;

  //central receive UUID
  while ( uart_svc.available() )
  {
    count = uart_svc.read(buf, 4);
    sprintf(&received_id[loopCount*4], "%s", buf);
  }
  
  loopCount++;

  //write to file
  if(loopCount == 9) {
    received_id[36] = '\0';
    while(mtx == 2) { ; } //wait for mutex
    Serial.println("[cent] storing received id");

    mtx = 1; //set the mutex
    if(!checkForDuplicates("day-1")) {
      writeUUID("day-1", false);
    }
    else {
      Serial.println("duplicate detected");
    }
    loopCount = 0;
    mtx = 0; //reset mutex
    centralReceived = true;
  }
  
}


void prph_connect_callback(uint16_t conn_handle)
{
  // Get the reference to current connection

  BLEConnection* connection = Bluefruit.Connection(conn_handle);

  //this chunk is really just for debugging
  char central_name[32] = { 0 };
  connection->getPeerName(central_name, sizeof(central_name));
  Serial.print("Connected to ");
  Serial.println(central_name);


  //peripheral send UUID
  Serial.println("Sending UUID");
  for (unsigned i = 0; i < 9; i++) {
    bleuart.write(&device_id[i*4], 4 );
  }
  Serial.println("Sent UUID");
}

//peripheral receive UUID
void bleuart_peripheral_rx_callback(uint16_t conn_handle)
{
  char buf[32];
  int count = 0;
  while (bleuart.available() )
  {
    count = bleuart.read(buf, 4);
    sprintf(&received_id[loopCount*4], "%s", buf);
  }
  
  loopCount++;

  //write to file
  if(loopCount == 9) {
    received_id[36] = '\0';
    while(mtx == 1) {;} // wait for mutex
    Serial.println("[prph] storing received id");
    mtx = 2; //set mutex
    if(!checkForDuplicates("day-1")) {
      writeUUID("day-1", false);
    }
    else {
      Serial.println("duplicate detected");
    }
    loopCount = 0;
    mtx = 0;
  }
}

//central is the one that disconnects, so it needs to reset everything
void cent_disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;
  
  Serial.println("[Cent] Disconnected");
  loopCount = 0;
  centralReceived = false;
  centralSent = false;
}

//peripheral just needs to reset loopCount in case connection drops in the middle of transmission
void prph_disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  // Serial.println();
  Serial.println("[Prph] Disconnected");
  loopCount = 0;
}
