import os
import cx_Freeze
import sys
import pyaudio
import threading
import socket
import vlc
import tkinter as tk
import time

# directory = '/mnt/d/yase/Final/executable/setup/'

build_option = {"packages":["tkinter","vlc", "vlc.MediaPlayer","time","pyaudio","threading","socket","os"], "include_files":['elec.ico', 'waves.wav', 'alarm.wav']}

summary_data = {"author": "CIT-U Electors", "comments":"Thesis project on BSECE", "keywords": "Wi-Fi, Networking, Socket, Python, Software"}

msi_option = {"install_icon": "elec.ico", 
"all_users": True, 
"target_name":"ReceiverAppInstaller", 
"summary_data": summary_data, 
"initial_target_dir": 'C:\\Program Files\\ReceiverApp'
}


base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("receiver.py", base=base, icon='elec.ico',
                shortcutDir="DesktopFolder", targetName="ReceiverApp", shortcutName="ReceiverApp")]

cx_Freeze.setup(
    name = "ElectorsReceiverApp",
    options = {"build_exe": build_option, "bdist_msi": msi_option},
    version = "1.1",
    description = "WiFi Speaker Application",
    executables = executables
    )