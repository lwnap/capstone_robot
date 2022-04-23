//char t[] = "";            // to receive information

#define ENA_m1 5        // Enable/speed motor back(breadboard) right  -> A-ENVA
#define ENB_m1 6        // Enable/speed motor back left               -> A-ENVB
#define ENA_m2 10       // Enable/speed motor front(arduino) right    -> B-ENVB
#define ENB_m2 11       // Enable/speed motor front left              -> B-ENVA

#define IN_11  2        // L298N #1 in 1 motor Back Right
#define IN_12  3        // L298N #1 in 2 motor Back Right
#define IN_13  4        // L298N #1 in 3 motor Back Left
#define IN_14  7        // L298N #1 in 4 motor Back Left

#define IN_21  8        // L298N #2 in 1 motor Front Left
#define IN_22  9        // L298N #2 in 2 motor Front Left
#define IN_23  12       // L298N #2 in 3 motor front right
#define IN_24  13       // L298N #2 in 4 motor front right

String a = "";
float sx = 0.0;       // start point x
float sy = 0.0;       // start point y
float ex = 5.0;       // end point x
float ey = 5.0;       // end point y



int speedCar = 80;
int delta = 25;
String t = ""; 

void goBackward(){
    digitalWrite(IN_11, HIGH);
    digitalWrite(IN_12, LOW);
    analogWrite(ENA_m1, speedCar);


    digitalWrite(IN_13, LOW);
    digitalWrite(IN_14, HIGH);
    analogWrite(ENB_m1, speedCar);


    digitalWrite(IN_21, HIGH);
    digitalWrite(IN_22, LOW);
    analogWrite(ENA_m2, speedCar);


    digitalWrite(IN_23, LOW);
    digitalWrite(IN_24, HIGH);
    analogWrite(ENB_m2, speedCar);
}

void goForward(){ 

    digitalWrite(IN_11, LOW);
    digitalWrite(IN_12, HIGH);
    analogWrite(ENA_m1, speedCar);

    digitalWrite(IN_13, HIGH);
    digitalWrite(IN_14, LOW);
    analogWrite(ENB_m1, speedCar);

    digitalWrite(IN_21, LOW);
    digitalWrite(IN_22, HIGH);
    analogWrite(ENA_m2, speedCar);

    digitalWrite(IN_23, HIGH);
    digitalWrite(IN_24, LOW);
    analogWrite(ENB_m2, speedCar);

  }

void stop(){
    digitalWrite(IN_11, LOW);
    digitalWrite(IN_12, LOW);
    analogWrite(ENA_m1, speedCar);


    digitalWrite(IN_13, LOW);
    digitalWrite(IN_14, LOW);
    analogWrite(ENB_m1, speedCar);


    digitalWrite(IN_21, LOW);
    digitalWrite(IN_22, LOW);
    analogWrite(ENA_m2, speedCar);

    
    digitalWrite(IN_23, LOW);
    digitalWrite(IN_24, LOW);
    analogWrite(ENB_m2, speedCar);
}

void turnLeft(){
    digitalWrite(IN_11, LOW);
    digitalWrite(IN_12, HIGH);
    analogWrite(ENA_m1, speedCar + delta);

    digitalWrite(IN_13, HIGH);
    digitalWrite(IN_14, LOW);
    analogWrite(ENB_m1, speedCar);

    digitalWrite(IN_21, LOW);
    digitalWrite(IN_22, HIGH);
    analogWrite(ENA_m2, speedCar + delta);

    digitalWrite(IN_23, HIGH);
    digitalWrite(IN_24, LOW);
    analogWrite(ENB_m2, speedCar);
  
}


void turnRight(){
    digitalWrite(IN_11, LOW);
    digitalWrite(IN_12, HIGH);
    analogWrite(ENA_m1, speedCar);

    digitalWrite(IN_13, HIGH);
    digitalWrite(IN_14, LOW);
    analogWrite(ENB_m1, speedCar + delta);

    digitalWrite(IN_21, LOW);
    digitalWrite(IN_22, HIGH);
    analogWrite(ENA_m2, speedCar);

    digitalWrite(IN_23, HIGH);
    digitalWrite(IN_24, LOW);
    analogWrite(ENB_m2, speedCar + delta);
  
}

void setup() {
    
    pinMode(ENA_m1, OUTPUT);
    pinMode(ENB_m1, OUTPUT);
    pinMode(ENA_m2, OUTPUT);
    pinMode(ENB_m2, OUTPUT);

  
    pinMode(IN_11, OUTPUT);    // Back Right forward
    pinMode(IN_12, OUTPUT);    // Back Right backward
    pinMode(IN_13, OUTPUT);    // Back Left forward
    pinMode(IN_14, OUTPUT);    // Back Left backward
    
    pinMode(IN_21, OUTPUT);    // Front Left forward
    pinMode(IN_22, OUTPUT);    // Front Left backward
    pinMode(IN_23, OUTPUT);    // Front Right forward
    pinMode(IN_24, OUTPUT);    // Front Right backward

    Serial.begin(9600);   // data rate to 9600 bps
    Serial.println("start");

}

void loop() {
  if(Serial.available()>0){
    t = Serial.readString();
    
    Serial.println(t);

    if (t == "l"){
      turnLeft();
      delay(1000);
      t = "*";
    }
    else if (t == "r"){
      turnRight();
      delay(1000);
      t = "*";
    }
    else if (t == "s"){
      stop();
      delay(1000);
      t = "*";
    }
    else{
      goForward();
      delay(1000);
      t = '*';
    }

//    if (t == '0'){
//      goForward();
//      delay(1000);
//      t = '*';
//    }
//    else if (t == '1'){
//      stop();
//      delay(1000);
//      t = '*';
//    }
//    else if (t == '2'){
//      goBackward();
//      delay(1000);
//      t = '*';
//    }
  }

  
}


//void setup() {
//  // put your setup code here, to run once:
//  Serial.begin(9600);
//  Serial.println("Arduino start");
//}
//
//void loop() {
//  // put your main code here, to run repeatedly:
//  if (Serial.available()>0){
//    a = Serial.readString();
////    Serial.println("signal receiving");
//    Serial.println(a);
////    Serial.println("signal received");
//
//  }
//}
