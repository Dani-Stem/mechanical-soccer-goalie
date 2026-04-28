#include <Servo.h>

Servo x_servo, y_servo; 

int a;
int horizontal = 45;

void setup() {
 
  x_servo.attach(3);  
  Serial.begin(9600); 
  // delay(1000);
}

void loop() 
{
  if(Serial.available()>0) 
  {
      a=Serial.read();                  
      if(a=='1')                       
       {                                
       horizontal=horizontal+5;
       x_servo.write(horizontal);
      //  delay(20);
       Serial.println("SHIFTING RIGHT...");
       }
      else if(a=='2')                 
      {
       horizontal=horizontal-5;
       x_servo.write(horizontal);
      //  delay(20);
       Serial.println("SHIFTING LEFT...");
      }
  }
}