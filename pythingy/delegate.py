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
from bluepy.btle import DefaultDelegate

import struct

class ThingyDelegate(DefaultDelegate):
    
    def DEBUG(self,msg):
        if self.debug is not False:
            print(msg)
    
    def __init__(self,thingy,debug=False):
        self.debug = debug
        self.thingy = thingy
        
    def handleNotification(self, hnd, data):
        if (hnd == self.thingy.environment.e_temperature_handle):
            temperature_int,temperature_dec = self._extract_temperature_data(data)
            self.DEBUG('Notification: Temp received:  {}.{} degCelcius'.format(temperature_int, temperature_dec))
            
        elif (hnd == self.thingy.environment.e_pressure_handle):
            pressure_int, pressure_dec = self._extract_pressure_data(data)
            self.DEBUG('Notification: Press received: {}.{} hPa'.format(
                        pressure_int, pressure_dec))

        elif (hnd == self.thingy.environment.e_humidity_handle):
            hymidity = self._extract_hymidity_data(data)
            self.DEBUG('Notification: Humidity received: {} %'.format(hymidity))

        elif (hnd == self.thingy.environment.e_gas_handle):
            eco2, tvoc = self._extract_gas_data(data)
            self.DEBUG('Notification: Gas received: eCO2 ppm: {}, TVOC ppb: {} %'.format(eco2, tvoc))

        elif (hnd == self.thingy.environment.e_color_handle):
            red, green, blue, clear = self._extract_color_data(data)
            self.DEBUG('Notification: Color: R: {}, G: {}, B: {}, C: {}'.format(red,green,blue,clear))            

        elif (hnd == self.thingy.ui.ui_button_handle):
            button = self._extract_button_data(data)
            self.DEBUG('Notification: Button state [1 -> released]: {}'.format(self._str_to_int(button)))

        elif (hnd == self.thingy.motion.m_tap_handle):
            direction, count = self._extract_tap_data(data)
            self.DEBUG('Notification: Tap: direction: {}, count: {}'.format(direction, count))

        elif (hnd == self.thingy.motion.m_orient_handle):
            orientation = self._extract_orientation_data(data)
            self.DEBUG('Notification: Orient: {}'.format(orientation))

        elif (hnd == self.thingy.motion.m_quaternion_handle):
            quaternion_w, quaternion_x, quaternion_y, quaternion_z = self._extract_quaternion_data(data)
            self.DEBUG('Notification: Quaternion: w: {}, x: {}, y: {}, z: {}'.format(quaternion_w,quaternion_x,quaternion_y,quaternion_z))

        elif (hnd == self.thingy.motion.m_stepcnt_handle):
            steps,ms = self._extract_step_data(data)
            self.DEBUG('Notification: Step Count: {}, ms: {}'.format(steps, ms))

        elif (hnd == self.thingy.motion.m_rawdata_handle):
            accel,gyro,comp = self._extract_raw_data(data)
            self.DEBUG('Notification: Raw data: accel:[{},{},{}] gyro:[{},{},{}] comp:[{},{},{}]'.format(accel[0],accel[1],accel[2],
                                                                                                        gyro[0],gyro[1],gyro[2],
                                                                                                        comp[0],comp[1],comp[2]))
        elif (hnd == self.thingy.motion.m_euler_handle):
            roll,pitch,yaw = self._extract_euler_data(data)
            self.DEBUG('Notification: Euler: roll:{}, pitch:{}, yaw:{}'.format(roll,pitch,yaw))
    
        elif (hnd == self.thingy.motion.m_rotation_handle):
            rot = self._extract_rotation_data(data)
            self.DEBUG('Notification: Rotation matrix: {}'.format(rot))

        elif (hnd == self.thingy.motion.m_heading_handle):
            heading = self._extract_heading_data(data)
            self.DEBUG('Notification: Heading: {}'.format(heading))

        elif (hnd == self.thingy.motion.m_gravity_handle):
            x,y,z = self._extract_gravity_data(data)
            self.DEBUG('Notification: Gravity: x:{}, y:{}, z:{}'.format(x,y,z))        

        elif (hnd == self.thingy.sound.s_speaker_status_handle):
	    status = self._extract_speaker_status_data(data)
            self.DEBUG('Notification: Speaker Status: {}'.format(status))

        elif (hnd == self.thingy.sound.s_microphone_handle):
            self.DEBUG('Notification: Microphone: {}'.format(teptep))

        elif (hnd == self.thingy.battery.b_battery_handle):
            battery = self._extract_battery_data()
            self.DEBUG('Notification: Battery: {}%'.format(battery))

        else:
            self.DEBUG('Notification: UNKOWN: hnd {}'.format(hnd))

    def _extract_button_data(self,data) 
	'''Extract button data'''
	button, = struct.unpack('B',data)
	return button

    def _extract_battery_data(self,data) 
	'''Extract battery data'''
	battery, = struct.unpack('B',data)
	return battery

    def _extract_temperature_data(self,data):
        '''Extract temperature data from data string'''
        temperature_int, = struct.unpack('b', data[0:1])
        temperature_dec, = struct.unpack('B', data[1:2])
        return temperature_int, temperature_dec
     
    def _extract_pressure_data(self, data):
        ''' Extract pressure data from data string. '''
        pressure_int, = struct.unpack('i', data[0:4])
        pressure_dec, = struct.unpack('B', data[4:5])
        return (pressure_int, pressure_dec)

    def _extract_hymidity_data(self, data):
        '''Extract humidity data from data string'''
        humidity, = struct.unpack('B', data)
        return humidity

    def _extract_gas_data(self, data):
        ''' Extract gas data from data string. '''
        eco2, = struct.unpack('H', data[0:2])
        tvoc, = struct.unpack('H', data[2:4])
        return eco2, tvoc

    def _extract_color_data(self,data):
        '''Extract color data from data string'''
        red,   =  struct.unpack('H', data[0:2])
        green, =  struct.unpack('H', data[2:4])
        blue,  =  struct.unpack('H', data[4:6])
        clear, =  struct.unpack('H', data[6:8])
        return red, green, blue, clear

    def _extract_tap_data(self, data):
        direction, = struct.unpack('B',data[0:1])
        count, = struct.unpack('B',data[1:2]) 
        return (direction, count)
    
    def _extract_orientation_data(self,data):
        orientation, = struct.unpack('B',data)
        return orientation
    
    def _extract_quaternion_data(self,data):
        w  = (struct.unpack('i', data[0:4])[0]  *1.0)/2**30
        x  = (struct.unpack('i', data[4:8])[0]  *1.0)/2**30
        y  = (struct.unpack('i', data[8:12])[0] *1.0)/2**30
        z  = (struct.unpack('i', data[12:16])[0]*1.0)/2**30
        return w,x,y,z
    
    def _extract_step_data(self,data):
        steps,  = struct.unpack('I', data[0:4])
        ms,     = struct.unpack('I', data[4:8])
        return steps,ms   
            
    def _extract_raw_data(self,data):
        acc_x  = (struct.unpack('h', data[0:2])[0]  *1.0)/2**10
        acc_y  = (struct.unpack('h', data[2:4])[0]  *1.0)/2**10
        acc_z  = (struct.unpack('h', data[4:6])[0]  *1.0)/2**10
        gyro_x = (struct.unpack('h', data[6:8])[0]  *1.0)/2**5
        gyro_y = (struct.unpack('h', data[8:10])[0] *1.0)/2**5
        gyro_z = (struct.unpack('h', data[10:12])[0]*1.0)/2**5
        comp_x = (struct.unpack('h', data[12:14])[0]*1.0)/2**4
        comp_y = (struct.unpack('h', data[14:16])[0]*1.0)/2**4
        comp_z = (struct.unpack('h', data[16:18])[0]*1.0)/2**4
        return [acc_x,acc_y,acc_z],[gyro_x,gyro_y,gyro_z],[comp_x,comp_y,comp_z]
    
    def _extract_euler_data(self,data):
        roll  = (struct.unpack('i', data[0:4])[0]  *1.0)/2**16
        pitch = (struct.unpack('i', data[4:8])[0] *1.0)/2**16
        yaw   = (struct.unpack('i', data[8:12])[0]*1.0)/2**16
        return roll,pitch,yaw
    
    def _extract_rotation_data(self,data):
        a11 = (struct.unpack('h', data[0:2])[0]  *1.0)/2**14
        a12 = (struct.unpack('h', data[2:4])[0]  *1.0)/2**14
        a13 = (struct.unpack('h', data[4:6])[0]  *1.0)/2**14
        a21 = (struct.unpack('h', data[6:8])[0]  *1.0)/2**14
        a22 = (struct.unpack('h', data[8:10])[0] *1.0)/2**14
        a23 = (struct.unpack('h', data[10:12])[0]*1.0)/2**14
        a31 = (struct.unpack('h', data[12:14])[0]*1.0)/2**14
        a32 = (struct.unpack('h', data[14:16])[0]*1.0)/2**14
        a33 = (struct.unpack('h', data[16:18])[0]*1.0)/2**14
        return [[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]]
         
    def _extract_heading_data(self,data): 
        heading, = (struct.unpack('i', data)[0]*1.0)/2**16
        return heading
    
    def _extract_gravity_data(self,data):
        x, = struct.unpack('f', data[0:4])
        y, = struct.unpack('f', data[4:8])
        z, = struct.unpack('f', data[8:12])
        return x,y,z

    def _extract_speaker_status_data(self,data):
        status, = struct.unpack('B',data)
	return status
