/*********************************************************************
 This is an example for our nRF52 based Bluefruit LE modules

 Pick one up today in the adafruit shop!

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!

 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/

/*
 * This sketch demonstrate the central API(). A additional bluefruit
 * that has bleuart as peripheral is required for the demo.
 */
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>
#include <Adafruit_TinyUSB.h>

using namespace Adafruit_LittleFS_Namespace;

#define IDSIZE 16
#define STRINGSIZE IDSIZE * 2 + 5

void generateguid(byte[]);
File file(InternalFS);
byte randomUuid[IDSIZE];
void setupfile(const char*, int);
void writefile(byte[]);
void printfileguids(const char*);




BLEClientBas  clientBas;  // battery client
BLEClientDis  clientDis;  // device information client
BLEClientUart clientUart; // bleuart client

void setup()
{
  Serial.begin(115200);
  randomSeed(6969);
//  while ( !Serial ) delay(10);   // for nrf52840 with native usb

  // Serial.println("Bluefruit52 Central BLEUART Example");
  // Serial.println("-----------------------------------\n");
  
  // Initialize Bluefruit with maximum connections as Peripheral = 0, Central = 1
  // SRAM usage required by SoftDevice will increase dramatically with number of connections
  Bluefruit.begin(0, 1);
  
  Bluefruit.setName("Bluefruit52 Central");

  // Configure Battyer client
  clientBas.begin();  

  // Configure DIS client
  clientDis.begin();

  // Init BLE Central Uart Serivce
  clientUart.begin();
  clientUart.setRxCallback(bleuart_rx_callback);

  // Increase Blink rate to different from PrPh advertising mode
  Bluefruit.setConnLedInterval(250);

  // Callbacks for Central
  Bluefruit.Central.setConnectCallback(connect_callback);
  Bluefruit.Central.setDisconnectCallback(disconnect_callback);

  /* Start Central Scanning
   * - Enable auto scan if disconnected
   * - Interval = 100 ms, window = 80 ms
   * - Don't use active scan
   * - Start(timeout) with timeout = 0 will scan forever (until connected)
   */
  Bluefruit.Scanner.setRxCallback(scan_callback);
  Bluefruit.Scanner.restartOnDisconnect(true);
  Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  Bluefruit.Scanner.useActiveScan(false);
  Bluefruit.Scanner.start(0);                   // // 0 = Don't stop scanning after n seconds
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
    // Serial.print("BLE UART service detected. Connecting ... ");

    // Connect to device with bleuart service in advertising
    Bluefruit.Central.connect(report);
  }else
  {      
    // For Softdevice v6: after received a report, scanner will be paused
    // We need to call Scanner resume() to continue scanning
    Bluefruit.Scanner.resume();
  }
}

/**
 * Callback invoked when an connection is established
 * @param conn_handle
 */
void connect_callback(uint16_t conn_handle)
{
  // Serial.println("Connected");


  // Serial.print("Discovering BLE Uart Service ... ");
  if ( clientUart.discover(conn_handle) )
  {
    // Serial.println("Found it");

    // Serial.println("Enable TXD's notify");
    clientUart.enableTXD();

    // Serial.println("Ready to receive from peripheral");
  }else
  {
    // Serial.println("Found NONE");
    
    // disconnect since we couldn't find bleuart service
    Bluefruit.disconnect(conn_handle);
  }  
}

/**
 * Callback invoked when a connection is dropped
 * @param conn_handle
 * @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
 */
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;
  
  // Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}

/**
 * Callback invoked when uart received data
 * @param uart_svc Reference object to the service where the data 
 * arrived. In this example it is clientUart
 */
char uuid[37];
int loopCount = 0;

void bleuart_rx_callback(BLEClientUart& uart_svc)
{
  //Serial.print("[RX]: ");
  char buf[32];
  int count = 0;
  while ( uart_svc.available() )
  {
    // uart_svc.readBytesUntil('\n', buf, 16);
    count = uart_svc.read(buf, 4);
    // Serial.write(buf, count);
    // memcpy(uuid, buf, count);
    sprintf(&uuid[loopCount*4], "%s", buf);
    // loopCount++;
  }
  
  //Serial.println(loopCount);
  loopCount++;

  if(loopCount == 9) {
    uuid[36] = '\n';
    setupfile("devicedata", 1);
    // Serial.print("UUID: ");
    // Serial.write(uuid, sizeof(uuid));
    // Serial.println();
    loopCount = 0;
  }
  
}

void loop()
{
  printfileguids("devicedata");
  delay(10000);
  if ( Bluefruit.Central.connected() )
  {
    // Not discovered yet
    if ( clientUart.discovered() )
    {
      
      // Discovered means in working state
      // Get Serial input and send to Peripheral
      if ( Serial.available() )
      {
        delay(2); // delay a bit for all characters to arrive
        
        char str[20+1] = { 0 };
        Serial.readBytes(str, 20);
        
        clientUart.print( str );
      }
    }
  }
}



void setupfile(const char* filename, int guidcount = 1) {
  file.open(filename, FILE_O_READ);
  if (file) {
    //Serial.println("Clearing Old File");
    file.close();
    InternalFS.remove(filename);
  }
  if (file.open(filename, FILE_O_WRITE)) {
    //Serial.println("New File Opend");
    //Serial.println("OK");

    // for (int j = 0; j < guidcount; j++) {
      //Serial.println("Genearting new guid");
      // generateguid(detectedguid);
      // char writestring[sizeof(uuid) * 2 + 1];

      // for (int i = 0; i < sizeof(detectedguid); i++) {
      //   sprintf(&writestring[i * 2], "%02X", uuid[i]);
      // }
      // writestring[sizeof(uuid) * 2] = '\n';

      file.write(uuid, sizeof(uuid));
    // }
    file.close();
  }
}

void generateguid(byte guid[]) {
  for (int i = 0; i < IDSIZE; i++) {
    guid[i] = random(256);
  }
}

void printfileguids(const char* filename) {
  Serial.println();
  // Serial.println("Printing File UUIDS");
  Serial.println(filename);
  file.open(filename, FILE_O_READ);
  if (file) {
    while (file.available()) {
      Serial.write(file.read());
    }
  }
}

// void writefile(byte guid[]) {
//   for (int i = 0; i < IDSIZE; i++) {
//     //Serial.print(guid[i], HEX);
//   }
//   //Serial.print('\n');
// }