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
├── LICENSE
├── README.md
├── requirements.txt
└── src
    ├── ContorlComputer.py # Computer control instructions implemented
    ├── HANDTRACKINGMODULE.py # Gesture recognition model
    └── main.py # Main program, responsible for communicating with esp32cam and recognizing specific gestures
```


