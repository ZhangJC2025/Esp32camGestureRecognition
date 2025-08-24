# Esp32camGestureRecognition

## Installation of [Esp32camWifiCam](https://github.com/yoursunny/esp32cam)

1. Install [ESP32 Arduino core](https://github.com/espressif/arduino-esp32) v3.x.
2. Clone [this repository](https://github.com/yoursunny/esp32cam) under `$HOME/Arduino/libraries` directory.
3. In *Tools* - *Board* menu, select **AI Thinker ESP32-CAM** to enable 4MB external PSRAM.
4. Add `#include <esp32cam.h>` to your sketch.
5. Check out the [examples of WifiCam](https://github.com/yoursunny/esp32cam/tree/main/examples/WifiCam) for how to use.

## Installation of GestureRecognition

1. Clone this repository.
2. Install Python 3.8.
3. Run `pip install -r requirements.txt`in terminal.

## Operation of Project
1. Check the IP address of Esp32cam in the Arduino serial monitor.
2. Modify the url variable in main.py to the IP address of Esp32cam
3. Run main.py





