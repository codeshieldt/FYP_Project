#include <hidboot.h>
#include <usbhub.h>
#include "Keyboard.h" //Keyboard Library

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef includeifneccessary
#include <spi4teensy3.h>
#include <SPI.h>
#endif

// Define the key codes for the left and right Windows (GUI) keys.
#define LEFT_GUI_MODIFIER 0x08
#define RIGHT_GUI_MODIFIER 0x80
#define BACKSPACE_KEY 0x2A

char keyasc;
int keycode;
boolean iskeypressed;
bool shift = false; //shift key state

class KbdRptParser : public KeyboardReportParser
{
public: //can be accessed anywhere
    uint8_t _parse(uint8_t key); //convert non-standard key codes to their corresponding standard key codes
    String _getChar(uint8_t key); //a key code as input and returns the corresponding character representation of that key
protected: //can be accessed only in the class and the derived or childern classes
  void OnControlKeysChanged(uint8_t before, uint8_t after);
  virtual void OnKeyDown  (uint8_t mod, uint8_t key);
  virtual void OnKeyUp(uint8_t mod, uint8_t key);
  void OnKeyPressed(uint8_t key);
};

void KbdRptParser::OnControlKeysChanged(uint8_t before, uint8_t after) {
  // If left GUI key was pressed
  if((before & LEFT_GUI_MODIFIER) == 0 && (after & LEFT_GUI_MODIFIER) != 0) {
    Serial.println("(WINDOW)");
  }

  // If right GUI key was pressed
  if((before & RIGHT_GUI_MODIFIER) == 0 && (after & RIGHT_GUI_MODIFIER) != 0) {
    Serial.println("(WINDOW)");
  }
}

void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key) {
  if (key == BACKSPACE_KEY) {
    Serial.println("(BACKSPACE)");
  }
  int parsedKey = _parse(key); // get the parsed key code
  if(parsedKey == key){ //parsed key code matches the original key code
    uint8_t c = OemToAscii(mod, key); //convert the key code to the corresponding ASCII character
    OnKeyPressed(c); //ASCII character as an argument
  }
}

void KbdRptParser::OnKeyUp(uint8_t mod, uint8_t key) {
  int parsedKey = _parse(key); // get the parsed key code
  if(parsedKey == key){ //parsed key code matches the original key code
    uint8_t c = OemToAscii(mod, key); //convert the key code to the corresponding ASCII character
    //OnKeyPressed(c); //ASCII character as an argument
  }
  else{
    Serial.print(_getChar(key)); // a string representation of the character associated with the key code
  }
}

void KbdRptParser::OnKeyPressed(uint8_t key)
{
keyasc = (char) key;
keycode = (int)key;
iskeypressed = true; 
};

uint8_t KbdRptParser::_parse(uint8_t key){
  /*
  Serial.print("0x");
  Serial.print(key, HEX);
  Serial.print(" = ");*/
  switch(key){
    case 40: return KEY_RETURN; break;
    case 41: return KEY_ESC; break;
    case 43: return KEY_TAB; break;
    case 58: return KEY_F1; break;
    case 59: return KEY_F2; break;
    case 60: return KEY_F3; break;
    case 61: return KEY_F4; break;
    case 62: return KEY_F5; break;
    case 63: return KEY_F6; break;    
    case 64: return KEY_F7; break;
    case 65: return KEY_F8; break;
    case 66: return KEY_F9; break;
    case 67: return KEY_F10; break;
    case 68: return KEY_F11; break;
    case 69: return KEY_F12; break;
    case 73: return KEY_INSERT; break;
    case 74: return KEY_HOME; break;
    case 75: return KEY_PAGE_UP; break;
    case 76: return KEY_DELETE; break;
    case 77: return KEY_END; break;
    case 78: return KEY_PAGE_DOWN; break;
    case 79: return KEY_RIGHT_ARROW; break;
    case 80: return KEY_LEFT_ARROW; break;
    case 81: return KEY_DOWN_ARROW; break;
    case 82: return KEY_UP_ARROW; break;
    case 88: return KEY_RETURN; break;
    //=====[DE-Keyboard]=====//
    case 0x64: return 236; break; // <
    case 0x32: return 92; break; // #
    //======================//
    default: {
      //Serial.print(" N/A ");
      return key;
    }
  }
}

String KbdRptParser::_getChar(uint8_t key){
 switch(key){
    case 40: return "(RETURN)\n"; break;
    case 41: return "(ESC)\n"; break;
    case 43: return "(TAB)\n"; break;
    case 58: return "(F1)\n"; break;
    case 59: return "(F2)\n"; break;
    case 60: return "(F3)\n"; break;
    case 61: return "(F4)\n"; break;
    case 62: return "(F5)\n"; break;
    case 63: return "(F6)\n"; break;    
    case 64: return "(F7)\n"; break;
    case 65: return "(F8)\n"; break;
    case 66: return "(F9)\n"; break;
    case 67: return "(F10)\n"; break;
    case 68: return "(F11)\n"; break;
    case 69: return "(F12)\n"; break;
    case 73: return "(INSERT)"; break;
    case 74: return "(HOME)\n"; break;
    case 75: return "(PAGE_UP)\n"; break;
    case 76: return "(DELETE)"; break;
    case 77: return "(END)\n"; break;
    case 78: return "(PAGE_DOWN)\n"; break;
    case 79: return "(RIGHT_ARROW)\n"; break;
    case 80: return "(LEFT_ARROW)\n"; break;
    case 81: return "(DOWN_ARROW)\n"; break;
    case 82: return "(UP_ARROW)\n"; break;
    case 88: return "(RETURN)\n"; break;
    //=====[DE-Keyboard]=====//
    case 0x64: {
      if(shift) return "<";
      else return ">";
      break;
    }
    case 0x32:{
      if(shift) return "'";
      else return "#";
      break;
    }
    //======================//
    default: {
      return "";
    }
  }
}

USB     Usb;
HIDBoot<USB_HID_PROTOCOL_KEYBOARD>    HidKeyboard(&Usb);

KbdRptParser Prs;

void setup()
{
  Serial.begin( 115200 );
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  if (Usb.Init() == -1)
    Serial.println("OSC did not start.");

  delay( 200 );

  HidKeyboard.SetReportParser(0, &Prs);
}

void loop()
{
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');
    
    if (message == "Requesting Connection..") {
      Serial.println("Connection Successful");
      Serial.println("Connected on COM port");
    }
  }
Usb.Task();
if(iskeypressed){
//Serial.println(keyasc);
Serial.println(keycode);
iskeypressed = false;  
}
}
