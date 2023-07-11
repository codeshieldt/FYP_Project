import serial
import serial.tools.list_ports
import keyboard
import random
import pyperclip
import time
from tkinter import *
import threading

def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports

def findArduino(portsFound):
    commPort = 'None'
    numConnection = len(portsFound)
    for i in range(0,numConnection):
        port = portsFound[i]
        strPort = str(port)
        if 'Arduino Leonardo' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
    if commPort is None:
        ports = list(get_ports())
        for port in ports:
            commPort = port.device
            print(port.device)
            ser = serial.Serial(commPort,baudrate = 115200, timeout=1)
            print(f"Checking port {commPort}")
            ser.write("Requesting Connection..\n".encode())
            response = ser.readline().decode().strip()
            if response == "Connection Successful":
                ser.write("Connected on COM port\n".encode())
                print(f"Connected on {commPort}")
    return commPort

def check_ports():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if connect_to_port(port.device):
            return port.device  # Return the connected port

def update_status():
    while True:
        portsFound = get_ports()
        connectPort = findArduino(portsFound)
        if connectPort != 'None':
            try:
                ser = serial.Serial(connectPort,baudrate = 115200, timeout=1)
                status.config(text=f'Connected to {connectPort}', fg='green')
                while True:
                    try:
                        line = ser.readline().decode().strip()
                    except (serial.SerialException, IOError):
                        status.config(text='Arduino disconnected', fg='red')
                        break
                    if line:
                        if line in key_map:
                            keyboard.press_and_release(key_map[line])
                        else:
                            try:
                                keycode = int(line)
                                character = chr(keycode)
                                pyperclip.copy(character)  
                                keyboard.press_and_release('ctrl+v') 
                                keystroke.config(text=f'ASCII: {keycode} - Character: {character}')
                            except ValueError:
                                pass
                ser.close()
            except (serial.SerialException, IOError):
                status.config(text='Cannot connect to the port', fg='red')
        else:
            status.config(text='No Arduino connected', fg='red')
        time.sleep(5)

# Mapping special keys to their functions
key_map = {
    "(RETURN)": 'enter',
    "(WINDOW)": 'cmd',
    "(ESC)": 'esc',
    "(BACKSPACE)": 'backspace',
    "(TAB)": 'tab',
    "(HOME)": 'home',
    "(PAGE_UP)": 'page up',
    "(DELETE)": 'delete',
    "(END)": 'end',
    "(PAGE_DOWN)": 'page down',
    "(RIGHT_ARROW)": 'right',
    "(LEFT_ARROW)": 'left',
    "(DOWN_ARROW)": 'down',
    "(UP_ARROW)": 'up',
    "(F1)": 'f1',
    "(F2)": 'f2',
    "(F3)": 'f3',
    "(F4)": 'f4',
    "(F5)": 'f5',
    "(F6)": 'f6',
    "(F7)": 'f7',
    "(F8)": 'f8',
    "(F9)": 'f9',
    "(F10)": 'f10',
    "(F11)": 'f11',
    "(F12)": 'f12'
}

# Create the main window
window = Tk()
window.title('Keystroke Receiver')

# Add some widgets
Label(window, text='Created by Dilawar and Sameer', font=('Arial', 16, 'bold')).pack(pady=10)
Canvas(window, width=400, height=3, bg='green').pack()
Label(window, text='Hardware anti-keyloggers protect you from keylogging attacks, which are\n'
                              'one of the most common and dangerous types of cyber threats.\n'
                              'They work by the concept of not generating the event of keystroking.',
                    font=('Arial', 12)).pack(pady=10)
Canvas(window, width=400, height=3, bg='green').pack()

status = Label(window, text='Checking connection...', font=('Arial', 12))
status.pack(pady=10)

keystroke = Label(window, text='', font=('Arial', 12))
keystroke.pack(pady=10)

# Start a new thread for checking the connection and updating the status
threading.Thread(target=update_status).start()

# Start the main loop
window.mainloop()
