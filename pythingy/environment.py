'''
The MIT License (MIT)

Copyright © 2018 ChevaierDeBalibari <chevalierdebalibari@keemail.me>

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
from .static import Nordic_UUID
from .static import write_uint16
from .static import write_uint8

from .uuid import ENVIRONMENT_SERVICE_UUID
from .uuid import E_TEMPERATURE_CHAR_UUID 
from .uuid import E_PRESSURE_CHAR_UUID
from .uuid import E_HUMIDITY_CHAR_UUID
from .uuid import E_GAS_CHAR_UUID
from .uuid import E_COLOR_CHAR_UUID
from .uuid import E_CONFIG_CHAR_UUID
from .uuid import CCCD_UUID

import binascii

class EnvironmentService():
    '''
    Environment service module. Instance the class and enable to get access to the Environment interface.
    '''
    serviceUUID =           Nordic_UUID(ENVIRONMENT_SERVICE_UUID)
    temperature_char_uuid = Nordic_UUID(E_TEMPERATURE_CHAR_UUID)
    pressure_char_uuid =    Nordic_UUID(E_PRESSURE_CHAR_UUID)
    humidity_char_uuid =    Nordic_UUID(E_HUMIDITY_CHAR_UUID)
    gas_char_uuid =         Nordic_UUID(E_GAS_CHAR_UUID)
    color_char_uuid =       Nordic_UUID(E_COLOR_CHAR_UUID)
    config_char_uuid =      Nordic_UUID(E_CONFIG_CHAR_UUID)

    def __init__(self, periph):
        self.periph = periph
        self.environment_service = None
        self.temperature_char = None
        self.temperature_cccd = None
        self.pressure_char = None
        self.pressure_cccd = None
        self.humidity_char = None
        self.humidity_cccd = None
        self.gas_char = None
        self.gas_cccd = None
        self.color_char = None
        self.color_cccd = None
        self.config_char = None
        self._e_color_handle = None
        self._e_gas_handle = None
        self._e_humidity_handle = None
        self._e_pressure_handle = None
        self._e_temperature_handle = None
        
    def enable(self):
        ''' Enables the class by finding the service and its characteristics. '''
        if self.environment_service is None:
            self.environment_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.temperature_char is None:
            self.temperature_char = self.environment_service.getCharacteristics(self.temperature_char_uuid)[0]
            self._e_temperature_handle = self.temperature_char.getHandle()
            self.temperature_cccd = self.temperature_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.pressure_char is None:
            self.pressure_char = self.environment_service.getCharacteristics(self.pressure_char_uuid)[0]
            self._e_pressure_handle = self.pressure_char.getHandle()
            self.pressure_cccd = self.pressure_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.humidity_char is None:
            self.humidity_char = self.environment_service.getCharacteristics(self.humidity_char_uuid)[0]
            self._e_humidity_handle = self.humidity_char.getHandle()
            self.humidity_cccd = self.humidity_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.gas_char is None:
            self.gas_char = self.environment_service.getCharacteristics(self.gas_char_uuid)[0]
            self._e_gas_handle = self.gas_char.getHandle()
            self.gas_cccd = self.gas_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.color_char is None:
            self.color_char = self.environment_service.getCharacteristics(self.color_char_uuid)[0]
            self._e_color_handle = self.color_char.getHandle()
            self.color_cccd = self.color_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.config_char is None:
            self.config_char = self.environment_service.getCharacteristics(self.config_char_uuid)[0]

    def set_temperature_notification(self, state):
        if self.temperature_cccd is not None:
            if state == True:
                self.temperature_cccd.write(b"\x01\x00", True)
            else:
                self.temperature_cccd.write(b"\x00\x00", True)

    def set_pressure_notification(self, state):
        if self.pressure_cccd is not None:
            if state == True:
                self.pressure_cccd.write(b"\x01\x00", True)
            else:
                self.pressure_cccd.write(b"\x00\x00", True)

    def set_humidity_notification(self, state):
        if self.humidity_cccd is not None:
            if state == True:
                self.humidity_cccd.write(b"\x01\x00", True)
            else:
                self.humidity_cccd.write(b"\x00\x00", True)

    def set_gas_notification(self, state):
        if self.gas_cccd is not None:
            if state == True:
                self.gas_cccd.write(b"\x01\x00", True)
            else:
                self.gas_cccd.write(b"\x00\x00", True)

    def set_color_notification(self, state):
        if self.color_cccd is not None:
            if state == True:
                self.color_cccd.write(b"\x01\x00", True)
            else:
                self.color_cccd.write(b"\x00\x00", True)

    def configure(self, temp_int=None, press_int=None, humid_int=None, gas_mode_int=None,
                        color_int=None, color_sens_calib=None):
        if temp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, temp_int, 0)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if press_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, press_int, 1)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if humid_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, humid_int, 2)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if gas_mode_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, gas_mode_int, 8)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if color_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, color_int, 3)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if color_sens_calib is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, color_sens_calib[0], 9)
            new_config = write_uint8(current_config, color_sens_calib[1], 10)
            new_config = write_uint8(current_config, color_sens_calib[2], 11)
            self.config_char.write(binascii.a2b_hex(new_config), True)

    def disable(self):
        self.set_temperature_notification(False)
        self.set_pressure_notification(False)
        self.set_humidity_notification(False)
        self.set_gas_notification(False)
        self.set_color_notification(False)
        
    @property
    def e_temperature_handle(self):
        return self._e_temperature_handle

    @property
    def e_humidity_handle(self):
        return self._e_humidity_handle

    @property
    def e_pressure_handle(self):
        return self._e_pressure_handle
    
    @property
    def e_gas_handle(self):
        return self._e_gas_handle
    
    @property
    def e_color_handle(self):
        return self._e_color_handle
