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
from .static import Nordic_UUID
from .static import write_uint16
from .static import write_uint8

from .uuid import MOTION_SERVICE_UUID
from .uuid import M_CONFIG_CHAR_UUID
from .uuid import M_TAP_CHAR_UUID
from .uuid import M_ORIENTATION_CHAR_UUID
from .uuid import M_QUATERNION_CHAR_UUID
from .uuid import M_STEP_COUNTER_UUID
from .uuid import M_RAW_DATA_CHAR_UUID
from .uuid import M_EULER_CHAR_UUID
from .uuid import M_ROTATION_MATRIX_CHAR_UUID
from .uuid import M_HEAIDNG_CHAR_UUID
from .uuid import M_GRAVITY_VECTOR_CHAR_UUID
from .uuid import CCCD_UUID

import binascii

class MotionService():
    '''
    Motion service module. Instance the class and enable to get access to the Motion interface.
    '''
    serviceUUID =           Nordic_UUID(MOTION_SERVICE_UUID)
    config_char_uuid =      Nordic_UUID(M_CONFIG_CHAR_UUID)
    tap_char_uuid =         Nordic_UUID(M_TAP_CHAR_UUID)
    orient_char_uuid =      Nordic_UUID(M_ORIENTATION_CHAR_UUID)
    quaternion_char_uuid =  Nordic_UUID(M_QUATERNION_CHAR_UUID)
    stepcnt_char_uuid =     Nordic_UUID(M_STEP_COUNTER_UUID)
    rawdata_char_uuid =     Nordic_UUID(M_RAW_DATA_CHAR_UUID)
    euler_char_uuid =       Nordic_UUID(M_EULER_CHAR_UUID)
    rotation_char_uuid =    Nordic_UUID(M_ROTATION_MATRIX_CHAR_UUID)
    heading_char_uuid =     Nordic_UUID(M_HEAIDNG_CHAR_UUID)
    gravity_char_uuid =     Nordic_UUID(M_GRAVITY_VECTOR_CHAR_UUID)

    def __init__(self, periph):
        self.periph = periph
        self.motion_service = None
        self.config_char = None
        self.tap_char = None
        self.tap_char_cccd = None
        self.orient_char = None
        self.orient_cccd = None
        self.quaternion_char = None
        self.quaternion_cccd = None
        self.stepcnt_char = None
        self.stepcnt_cccd = None
        self.rawdata_char = None
        self.rawdata_cccd = None
        self.euler_char = None
        self.euler_cccd = None
        self.rotation_char = None
        self.rotation_cccd = None
        self.heading_char = None
        self.heading_cccd = None
        self.gravity_char = None
        self.gravity_cccd = None
        self._m_euler_handle = None
        self._m_gravity_handle = None
        self._m_heading_handle = None
        self._m_orient_handle = None
        self._m_quaternion_handle = None
        self._m_rawdata_handle = None
        self._m_rotation_handle = None
        self._m_stepcnt_handle = None
        self._m_tap_handle = None  
    
    def enable(self):
        ''' Enables the class by finding the service and its characteristics. '''
        if self.motion_service is None:
            self.motion_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.config_char is None:
            self.config_char = self.motion_service.getCharacteristics(self.config_char_uuid)[0]
        if self.tap_char is None:
            self.tap_char = self.motion_service.getCharacteristics(self.tap_char_uuid)[0]
            self._m_tap_handle = self.tap_char.getHandle()
            self.tap_char_cccd = self.tap_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.orient_char is None:
            self.orient_char = self.motion_service.getCharacteristics(self.orient_char_uuid)[0]
            self._m_orient_handle = self.orient_char.getHandle()
            self.orient_cccd = self.orient_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.quaternion_char is None:
            self.quaternion_char = self.motion_service.getCharacteristics(self.quaternion_char_uuid)[0]
            self._m_quaternion_handle = self.quaternion_char.getHandle()
            self.quaternion_cccd = self.quaternion_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.stepcnt_char is None:
            self.stepcnt_char = self.motion_service.getCharacteristics(self.stepcnt_char_uuid)[0]
            self._m_stepcnt_handle = self.stepcnt_char.getHandle()
            self.stepcnt_cccd = self.stepcnt_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.rawdata_char is None:
            self.rawdata_char = self.motion_service.getCharacteristics(self.rawdata_char_uuid)[0]
            self._m_rawdata_handle = self.rawdata_char.getHandle()
            self.rawdata_cccd = self.rawdata_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.euler_char is None:
            self.euler_char = self.motion_service.getCharacteristics(self.euler_char_uuid)[0]
            self._m_euler_handle = self.euler_char.getHandle()
            self.euler_cccd = self.euler_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.rotation_char is None:
            self.rotation_char = self.motion_service.getCharacteristics(self.rotation_char_uuid)[0]
            self._m_rotation_handle = self.rotation_char.getHandle()
            self.rotation_cccd = self.rotation_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.heading_char is None:
            self.heading_char = self.motion_service.getCharacteristics(self.heading_char_uuid)[0]
            self._m_heading_handle = self.heading_char.getHandle()
            self.heading_cccd = self.heading_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.gravity_char is None:
            self.gravity_char = self.motion_service.getCharacteristics(self.gravity_char_uuid)[0]
            self._m_gravity_handle = self.gravity_char.getHandle()
            self.gravity_cccd = self.gravity_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def set_tap_notification(self, state):
        if self.tap_char_cccd is not None:
            if state == True:
                self.tap_char_cccd.write(b"\x01\x00", True)
            else:
                self.tap_char_cccd.write(b"\x00\x00", True)

    def set_orient_notification(self, state):
        if self.orient_cccd is not None:
            if state == True:
                self.orient_cccd.write(b"\x01\x00", True)
            else:
                self.orient_cccd.write(b"\x00\x00", True)

    def set_quaternion_notification(self, state):
        if self.quaternion_cccd is not None:
            if state == True:
                self.quaternion_cccd.write(b"\x01\x00", True)
            else:
                self.quaternion_cccd.write(b"\x00\x00", True)

    def set_stepcnt_notification(self, state):
        if self.stepcnt_cccd is not None:
            if state == True:
                self.stepcnt_cccd.write(b"\x01\x00", True)
            else:
                self.stepcnt_cccd.write(b"\x00\x00", True)

    def set_rawdata_notification(self, state):
        if self.rawdata_cccd is not None:
            if state == True:
                self.rawdata_cccd.write(b"\x01\x00", True)
            else:
                self.rawdata_cccd.write(b"\x00\x00", True)

    def set_euler_notification(self, state):
        if self.euler_cccd is not None:
            if state == True:
                self.euler_cccd.write(b"\x01\x00", True)
            else:
                self.euler_cccd.write(b"\x00\x00", True)

    def set_rotation_notification(self, state):
        if self.rotation_cccd is not None:
            if state == True:
                self.rotation_cccd.write(b"\x01\x00", True)
            else:
                self.rotation_cccd.write(b"\x00\x00", True)

    def set_heading_notification(self, state):
        if self.heading_cccd is not None:
            if state == True:
                self.heading_cccd.write(b"\x01\x00", True)
            else:
                self.heading_cccd.write(b"\x00\x00", True)

    def set_gravity_notification(self, state):
        if self.gravity_cccd is not None:
            if state == True:
                self.gravity_cccd.write(b"\x01\x00", True)
            else:
                self.gravity_cccd.write(b"\x00\x00", True)

    def configure(self, step_int=None, temp_comp_int=None, magnet_comp_int=None,
                        motion_freq=None, wake_on_motion=None):
        if step_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, step_int, 0)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if temp_comp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, temp_comp_int, 1)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if magnet_comp_int is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, magnet_comp_int, 2)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if motion_freq is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint16(current_config, motion_freq, 3)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if wake_on_motion is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, wake_on_motion, 8)
            self.config_char.write(binascii.a2b_hex(new_config), True)

    def disable(self):
        self.set_tap_notification(False)
        self.set_orient_notification(False)
        self.set_quaternion_notification(False)
        self.set_stepcnt_notification(False)
        self.set_rawdata_notification(False)
        self.set_euler_notification(False)
        self.set_rotation_notification(False)
        self.set_heading_notification(False)
        self.set_gravity_notification(False)
        
    @property
    def m_tap_handle(self):
        return self._m_tap_handle
    
    @property
    def m_orient_handle(self):
        return self._m_orient_handle

    @property
    def m_quaternion_handle(self):
        return self._m_quaternion_handle
    
    @property
    def m_stepcnt_handle(self):
        return self._m_stepcnt_handle

    @property
    def m_rawdata_handle(self):
        return self._m_rawdata_handle
    
    @property
    def m_euler_handle(self):
        return self._m_euler_handle
    
    @property
    def m_rotation_handle(self):
        return self._m_rotation_handle
    
    @property
    def m_heading_handle(self):
        return self._m_heading_handle
    
    @property
    def m_gravity_handle(self):
        return self._m_gravity_handle    
