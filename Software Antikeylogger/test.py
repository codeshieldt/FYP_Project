import os
import sys
import ctypes
import psutil
import winreg

class AntiKeylogger:
    def __init__(self):
        self.keylogger_process_name = "MicrosoftVisualC++2012Redistributable-x86.exe"
        self.keylogger_registry_key = "Redistributable-x86"
        self.keylogger_registry_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'

    def kill_keylogger(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.keylogger_process_name:
                p = psutil.Process(proc.info['pid'])
                p.terminate()

    def delete_keylogger(self):
        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                if file == self.keylogger_process_name:
                    os.remove(os.path.join(root, file))

    def delete_registry_key(self):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.keylogger_registry_path, 0, winreg.KEY_WRITE) as key:
            try:
                winreg.DeleteValue(key, self.keylogger_registry_key)
            except WindowsError:
                pass

    def start(self):
        self.kill_keylogger()
        self.delete_keylogger()
        self.delete_registry_key()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        AntiKeylogger().start()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
