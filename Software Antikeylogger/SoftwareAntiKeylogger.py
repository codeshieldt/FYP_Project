import tkinter as tk
import os
import ctypes
import winreg
import psutil
import sys
import subprocess

# Keylogger information
keylogger_process_name = 'MicrosoftVisualC++2012Redistributable-x86.exe'
drive_path = "C:\\"
registry_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def remove_keylogger_from_filesystem():
    for dirpath, dirnames, filenames in os.walk(drive_path):
        for file in filenames:
            if file in keylogger_process_name:
                file_path = os.path.join(dirpath, file)
                os.remove(file_path)
                log_text.insert(tk.END, "Removed keylogger file.\n")

def remove_keylogger_from_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, 'Redistributable-x86')
        winreg.CloseKey(key)
        log_text.insert(tk.END, "Removed keylogger from registry.\n")
    except WindowsError:
        log_text.insert(tk.END, "Failed to remove keylogger from registry or it wasn't present.\n")

def remove_keylogger_from_processes():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == keylogger_process_name:
            process.kill()
            log_text.insert(tk.END, f"Suspicious process {process.info['name']} has been terminated.\n")
            return

    log_text.insert(tk.END, "Keylogger process not found or already terminated.\n")

def remove_keylogger():
    log_text.delete(1.0, tk.END)
    remove_keylogger_from_filesystem()
    remove_keylogger_from_registry()
    remove_keylogger_from_processes()

def run_with_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Create the main window
window = tk.Tk()
window.title("Software AntiKeylogger")
window.geometry("700x350")
window.configure(bg="black")

# Create the title label
title_label = tk.Label(window, text="Software AntiKeylogger", fg="green", bg="black", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Create the greetings message
greetings_label = tk.Label(window, text="Presented by Dilawar and Sameer", fg="green", bg="black", font=("Arial", 12))
greetings_label.pack()

# Create a separator line
separator = tk.Frame(window, height=2, width=400, bg="green")
separator.pack(pady=10)

# Create the definition label
definition_label = tk.Label(window, text="Keylogger Definition:", fg="green", bg="black", font=("Arial", 12, "bold"))
definition_label.pack()

# Create the definition text
definition_text = tk.Label(window, text="A keylogger is a type of surveillance software that records keystrokes made on a device.", fg="green", bg="black", font=("Arial", 12))
definition_text.pack()

# Create the published keyloggers label
keyloggers_label = tk.Label(window, text="Published Keyloggers:", fg="green", bg="black", font=("Arial", 12, "bold"))
keyloggers_label.pack()

# Create the published keyloggers text
keyloggers_text = tk.Label(window, text="KidInspector, Clever, Spyrix", fg="green", bg="black", font=("Arial", 12))
keyloggers_text.pack()

# Create a separator line
separator = tk.Frame(window, height=2, width=400, bg="green")
separator.pack(pady=10)

# Create the remove keylogger button
remove_button = tk.Button(window, text="Remove Keylogger", command=remove_keylogger, fg="green", bg="black", font=("Arial", 12, "bold"))
remove_button.pack()

# Create the log text
log_text = tk.Text(window, fg="green", bg="black", font=("Arial", 10), width=40, height=8)
log_text.pack(pady=10)

# Check admin privileges and run the program accordingly
if is_admin():
    remove_keylogger()
else:
    run_with_admin()

# Run the GUI main loop
window.mainloop()
