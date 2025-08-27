# Esp32camGestureRecognition

The computer can be controlled by gesture recognition, such as giving the computer a middle finger to shut it down.

## Installation
  ### Installation of [Esp32camWifiCam](https://github.com/yoursunny/esp32cam)
  
  1. Install [ESP32 Arduino core](https://github.com/espressif/arduino-esp32) v3.x.
  2. Clone [this repository](https://github.com/yoursunny/esp32cam) under `$HOME/Arduino/libraries` directory.
  3. In *Tools* - *Board* menu, select **AI Thinker ESP32-CAM** to enable 4MB external PSRAM.
  4. Add `#include <esp32cam.h>` to your sketch.
  5. Check out the [examples of WifiCam](https://github.com/yoursunny/esp32cam/tree/main/examples/WifiCam) for how to use.
  
  ### Installation of GestureRecognition
  
  1. Clone this repository.
  2. Install [Python](https://www.python.org) 3.8.
  3. Run `pip install -r requirements.txt`in terminal.
  
  ### Operation of Project
  1. Check the IP address of Esp32cam in the [Arduino](https://www.arduino.cc) serial monitor.
  2. Modify the url variable in main.py to the IP address of Esp32cam
  3. Run main.py

## Framework
```
.
├── hand-landmarks.png # Schematic diagram of the numbering of each joint in mediapipe
├── LICENSE # License File
├── README.md # Documentation
├── requirements.txt # Python Dependencies
└── src # Source Code
    ├── ContorlComputer.py # Computer control instructions implemented
    ├── HANDTRACKINGMODULE.py # Gesture recognition model
    └── main.py # Main program, responsible for communicating with esp32cam and recognizing specific gestures
```

# Esp32cam手势识别系统

通过手势识别控制计算机，例如向计算机竖中指即可将其关机。

## 安装说明
### 安装 [Esp32camWifiCam](https://github.com/yoursunny/esp32cam)
  
1. 安装 [ESP32 Arduino 核心库](https://github.com/espressif/arduino-esp32) v3.x 版本
2. 将[该代码库](https://github.com/yoursunny/esp32cam)克隆到 `$HOME/Arduino/libraries` 目录下
3. 在 *工具* - *开发板* 菜单中选择 **AI Thinker ESP32-CAM** 以启用4MB外部PSRAM
4. 在您的工程中添加 `#include <esp32cam.h>` 头文件
5. 查看 [WifiCam示例](https://github.com/yoursunny/esp32cam/tree/main/examples/WifiCam) 了解使用方法

### 安装手势识别组件
  
1. 克隆本代码库
2. 安装 [Python](https://www.python.org) 3.8 或更高版本
3. 在终端中运行 `pip install -r requirements.txt` 安装依赖

### 项目运行
1. 在 [Arduino](https://www.arduino.cc) 串口监视器中查看Esp32cam的IP地址
2. 将main.py中的url变量修改为Esp32cam的IP地址
3. 运行main.py主程序

## 项目结构
```
.
├── hand-landmarks.png # MediaPipe中各关节编号示意图
├── LICENSE # 许可证文件
├── README.md # 说明文档
├── requirements.txt # Python依赖列表
└── src # 源代码目录
    ├── ContorlComputer.py # 计算机控制指令实现
    ├── HANDTRACKINGMODULE.py # 手势识别模型
    └── main.py # 主程序，负责与esp32cam通信并识别特定手势
```
