import os
import sys

def shutdown():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        os.system("shutdown -h now")
    elif sys.platform.startswith('win'):
        os.system("shutdown /s /t 1")
    else:
        raise Exception('Unable to identify the current system')