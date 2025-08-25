import os
import sys
import platform


def control_computer(command):
    """Control the computer to perform specific operations"""
    commands = {
        "shutdown": {
            "linux": "shutdown -h now",
            "darwin": "shutdown -h now",  # macOS
            "win": "shutdown /s /t 1"
        },
        "restart": {
            "linux": "reboot",
            "darwin": "reboot",  # macOS
            "win": "shutdown /r /t 1"
        }
    }

    if command not in commands:
        raise ValueError(f"Unsupported command: {command}")

    system_type = None
    if sys.platform.startswith('linux'):
        system_type = "linux"
    elif sys.platform.startswith('darwin'):
        system_type = "darwin"
    elif sys.platform.startswith('win'):
        system_type = "win"

    if not system_type or system_type not in commands[command]:
        raise OSError(f"Current system does not support {command} operation")

    os.system(commands[command][system_type])