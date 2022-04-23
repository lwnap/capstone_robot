#include<SoftwareSerial.h>
//
#define TxD 2
#define RxD 3

SoftwareSerial mybt(TxD, RxD);

int t;
//int LED_BUILTIN; 


void setup(){
    pinMode(LED_BUILTIN, OUTPUT);
//    bluetoothSerial.begin(38400);
    Serial.begin(9600);   // data rate to 9600 bps
    mybt.begin(9600);
    Serial.println("start");
}

void loop(){

//    if(Serial.available()){
      if(mybt.available()){
        t = mybt.read();
        mybt.println(t);

      }
      if(t == '1') {           //Checks whether value of Incoming_value is equal to 1 
        digitalWrite(LED_BUILTIN, HIGH);  //If value is 1 then LED turns ON
        mybt.println("LED On"); 
        t = '*';
      }
      else if(t == '0'){       //Checks whether value of Incoming_value is equal to 0
        digitalWrite(LED_BUILTIN, LOW);   //If value is 0 then LED turns OFF
        mybt.println("LED Off");
        t = '*';

      } 

  }
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(1000);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//  delay(1000);   
//}
