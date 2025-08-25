import os
import sys
import platform


def control_computer(command):
    """控制计算机执行特定操作"""
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
        raise ValueError(f"不支持的命令: {command}")

    system_type = None
    if sys.platform.startswith('linux'):
        system_type = "linux"
    elif sys.platform.startswith('darwin'):
        system_type = "darwin"
    elif sys.platform.startswith('win'):
        system_type = "win"

    if not system_type or system_type not in commands[command]:
        raise OSError(f"当前系统不支持 {command} 操作")

    os.system(commands[command][system_type])