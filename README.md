# pythingy - Library for Nordic Semiconductor Thingy52 kit

This library lets you easily interface RaspberryPi with Nordic Semiconductor Thingy52. It is heavily based on Thingy52 example from bluepy library but this one is made as a separate package. Package is still in beta testing phase, so use it on your own risk. 

## Functionality 
Library supports several different measurements from the Thingy52:
* Temperature
* Humidity
* Pressure
* Gas (Air Quality)
* Color
* Button
* Tap
* Orientation
* Quaternion
* Step counter
* Raw accelerometer, gyroscope and magnetometer data
* Euler
* Rotation matrix
* Heading
* Gravity
* Speaker status
* Microphone 

To use this library you will need a Bluetooth Low Energy dongle attached to your computer and
Nordic Semiconductor Thingy52 kit. Library also require bluepy library to be installed.
Library is compatible with both Python 2.x and 3.x versions.

## Installation
To install pythingy library you need to clone repository and run pip installer:
```
git clone https://github.com/ChevalierDeBalibari/pythingy
cd pythingy
pip install bluepy
pip install . 
```
## Demo
To scan for your Thingy52 devices run following command:
```
sudo hcitool lescan
```
To connect to your Thingy52 run demo.py with one or more arguments to enable coresponding notifications: 
```
sudo python demo.py [arguments] XX:XX:XX:XX:XX:XX

positional arguments:
  mac_address    MAC address of BLE peripheral

optional arguments:
  -t T           time between polling
  --temperature  
  --pressure
  --humidity
  --gas
  --color
  --keypress
  --tap
  --orientation
  --quaternion
  --stepcnt
  --rawdata
  --euler
  --rotation
  --heading
  --gravity
  --battery
  --speaker
  --microphone
```
## Delegate

ThingyDelgate is an example for parsing and handling data. You can define your own delegate using following structure. 
Delegate will inherit all extraction functions and you can define your custom notification handler:
```
class MyThingyDelegate(ThingyDelgate):
    def handleNotification(self,hnd,data):
    ...
```
## Known issues
Thingy52 hungs when raw motion data notification is turned on after few minutes. 

## Conttributing
please have a look at [CONTRIBUTING.md](CONTRIBUTING.md)
