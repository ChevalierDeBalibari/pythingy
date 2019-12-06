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
from .uuid import BATTERY_SERVICE_UUID 
from .uuid import BATTERY_LEVEL_UUID
from .uuid import CCCD_UUID

from bluepy.btle import UUID

class BatterySensor():
    '''
    Battery Service module. Instance the class and enable to get access to Battery interface.
    '''
    serviceUUID = UUID(BATTERY_SERVICE_UUID)  # Ref https://www.bluetooth.com/specifications/gatt/services 
    battery_char_uuid = UUID(BATTERY_LEVEL_UUID) # Ref https://www.bluetooth.com/specifications/gatt/characteristics

    def __init__(self, periph):
        self.periph = periph
        self.battery_service = None
        self.battery_char = None
        self.battery_cccd = None
        self._b_battery_handle = None
        
    def enable(self):
        ''' Enables the class by finding the service and its characteristics. '''
        if self.battery_service is None:
            self.battery_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.battery_char is None:
            self.battery_char = self.battery_service.getCharacteristics(self.battery_char_uuid)[0]
            self._b_battery_handle = self.battery_char.getHandle()
            self.battery_cccd = self.battery_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def set_battery_notification(self, state):
        if self.battery_cccd is not None:
            if state == True:
                self.battery_cccd.write(b"\x01\x00", True)
            else:
                self.battery_cccd.write(b"\x00\x00", True)
    
    def disable(self):
        ''' Disable battery service notifications '''
        self.set_battery_notification(False)
        
    def read(self):
        ''' Returns the battery level in percent '''
        val = ord(self.data.read())
        return val
    
    @property
    def b_battery_handle(self):
        return self._b_battery_handle
