
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library

#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0

#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin

// Assign human-readable names to some common 16-bit color values:
#define	BLACK   0x0000
#define	BLUE    0x001F
#define	RED     0xF800
#define	GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

int total_time = 5;
int time;

void show_end(){
  tft.setRotation(1);
  tft.fillScreen(BLACK);
  tft.setTextColor(WHITE);
  tft.setTextSize(3);
  tft.setCursor(45,40);
  tft.println("Cet appareil");
  tft.setCursor(30,75);
  tft.println("est trop vieux");

  tft.setTextSize(3);
  tft.setCursor(0,140);
  tft.println("Jetez-le et allezen acheter un    autre.");
  delay(10000);
}

void set_style(){
  tft.setRotation(1);
  tft.fillScreen(BLACK);
  tft.setTextColor(WHITE);
  tft.setTextSize(8);
  tft.setCursor(35,90);
}

String get_str_time(){
  int min = time/60;
  int sec = time%60;
  String str_min = String(min);
  String str_sec = String(sec);
  if(min<10){
    str_min = "0"+String(min);
  }
  if(sec<10){
    str_sec = "0"+String(sec);
  }
  String to_return = str_min+":"+str_sec;
  return to_return;
}

void setup() {
  Serial.begin(9600);

  tft.reset();

  uint16_t identifier = tft.readID();

  tft.begin(identifier);

  time = total_time;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
  String to_print = get_str_time();

  if(to_print=="00:00"){
    show_end();
    time = total_time;
  } else {
    set_style();
    tft.println(to_print);
    delay(1000);
    time=time-1;
  }

  

}
