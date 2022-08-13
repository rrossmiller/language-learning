#include <Arduino.h>
#include <LiquidCrystal.h>

const int rs = 12, 
          en = 11, 
          d4 = 5, 
          d5 = 4, 
          d6 = 3, 
          d7 = 2;
unsigned int i = 0;
// const String messages[] = {"Hey, Mar", "Je t'aime"};
const String messages[] = {"Hey, Mar", "bisous"};
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
}

void loop() {

  for(String m: messages){
    lcd.setCursor(16,0);
    lcd.print(m);
    for(auto i=0; i < 16+m.length(); i++){
      lcd.scrollDisplayLeft();
      delay(400);
    }
    lcd.clear();
  }
}