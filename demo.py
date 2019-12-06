'''
The MIT License (MIT)

Copyright © 2018 Nebojsa Stojiljkovic <nebojsa@keemail.me>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from pythingy import Thingy52, ThingyDelegate
import argparse
import time
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mac_address', action='store', help='MAC address of BLE peripheral')
    parser.add_argument('-t',action='store',type=float, default=2.0, help='time between polling')
    parser.add_argument('--temperature', action="store_true",default=False)
    parser.add_argument('--pressure', action="store_true",default=False)
    parser.add_argument('--humidity', action="store_true",default=False)
    parser.add_argument('--gas', action="store_true",default=False)
    parser.add_argument('--color', action="store_true",default=False)
    parser.add_argument('--keypress', action='store_true', default=False)
    parser.add_argument('--tap', action='store_true', default=False)
    parser.add_argument('--orientation', action='store_true', default=False)
    parser.add_argument('--quaternion', action='store_true', default=False)
    parser.add_argument('--stepcnt', action='store_true', default=False)
    parser.add_argument('--rawdata', action='store_true', default=False)
    parser.add_argument('--euler', action='store_true', default=False)
    parser.add_argument('--rotation', action='store_true', default=False)
    parser.add_argument('--heading', action='store_true', default=False)
    parser.add_argument('--gravity', action='store_true', default=False)
    parser.add_argument('--battery', action='store_true', default=False)
    parser.add_argument('--speaker', action='store_true', default=False)
    parser.add_argument('--microphone', action='store_true', default=False)
    args = parser.parse_args()
    
    print('Connecting to ' + args.mac_address)
    thingy = Thingy52(args.mac_address)
    print('Connected...')
    try:
        # Set LED so that we know we are connected
        thingy.ui.enable()
        thingy.ui.set_led_mode_breathe(0x01, 50, 100) # 0x01 = RED
        print('LED set to breathe mode...')
    except Exception as ex:
        print(ex)
        sys.exit(1)
    try:    
        # Enabling selected sensors
        print('Enabling selected sensors...')
        # Environment Service
        if args.temperature:
            thingy.environment.enable()
            thingy.environment.configure(temp_int=1000)
            thingy.environment.set_temperature_notification(True)
        if args.pressure:
            thingy.environment.enable()
            thingy.environment.configure(press_int=1000)
            thingy.environment.set_pressure_notification(True)
        if args.humidity:
            thingy.environment.enable()
            thingy.environment.configure(humid_int=1000)
            thingy.environment.set_humidity_notification(True)
        if args.gas:
            thingy.environment.enable()
            thingy.environment.configure(gas_mode_int=1)
            thingy.environment.set_gas_notification(True)
        if args.color:
            thingy.environment.enable()
            thingy.environment.configure(color_int=1000)
            thingy.environment.configure(color_sens_calib=[0,0,0])
            thingy.environment.set_color_notification(True)
        # User Interface Service
        if args.keypress:
            thingy.ui.enable()
            thingy.ui.set_btn_notification(True)
        if args.battery:
            thingy.battery.enable()
            thingy.battery.set_battery_notification(True)
        # Motion Service
        if args.tap:
            thingy.motion.enable()
            thingy.motion.configure(motion_freq=200)
            thingy.motion.set_tap_notification(True)
        if args.orientation:
            thingy.motion.enable()
            thingy.motion.set_orient_notification(True)
        if args.quaternion:
            thingy.motion.enable()
            thingy.motion.set_quaternion_notification(True)
        if args.stepcnt:
            thingy.motion.enable()
            thingy.motion.configure(step_int=100)
            thingy.motion.set_stepcnt_notification(True)
        if args.rawdata:
            thingy.motion.enable()
            thingy.motion.set_rawdata_notification(True)
        if args.euler:
            thingy.motion.enable()
            thingy.motion.set_euler_notification(True)
        if args.rotation:
            thingy.motion.enable()
            thingy.motion.set_rotation_notification(True)
        if args.heading:
            thingy.motion.enable()
            thingy.motion.set_heading_notification(True)
        if args.gravity:
            thingy.motion.enable()
            thingy.motion.set_gravity_notification(True)
        # Sound Service
        if args.speaker:
            thingy.sound.enable()
            thingy.sound.configure(speaker_mode=0x03)
            thingy.sound.set_speaker_status_notification(True)
        # Test speaker
            thingy.sound.play_speaker_sample(1)
        if args.microphone:
            thingy.sound.enable()
            thingy.sound.configure(microphone_mode=0x01)
            thingy.sound.set_microphone_notification(True)

        # Allow sensors time to start up (might need more time for some sensors to be ready)
        print('All requested sensors and notifications are enabled...')
        thingy.setDelegate(ThingyDelegate(thingy,debug=True))
        time.sleep(1.0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
        
    try:
        while True:
            thingy.waitForNotifications(args.t)
    except KeyboardInterrupt:
        print("Keyboard interrupt... exiting")
    finally:
        thingy.disconnect()
        del thingy
        
if __name__ == "__main__":
    main()
                
