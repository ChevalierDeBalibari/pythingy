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

from .uuid import USER_INTERFACE_SERVICE_UUID
from .uuid import UI_LED_CHAR_UUID
from .uuid import UI_BUTTON_CHAR_UUID
from .uuid import CCCD_UUID

import binascii

class UserInterfaceService():
    '''
    User interface service module. Instance the class and enable to get access to the UI interface.
    '''
    serviceUUID = Nordic_UUID(USER_INTERFACE_SERVICE_UUID)
    led_char_uuid = Nordic_UUID(UI_LED_CHAR_UUID)
    btn_char_uuid = Nordic_UUID(UI_BUTTON_CHAR_UUID)
    # To be added: EXT PIN CHAR

    def __init__(self, periph):
        self.periph = periph
        self.ui_service = None
        self.led_char = None
        self.btn_char = None
        self.btn_char_cccd = None
        self._ui_button_handle = None
        # To be added: EXT PIN CHAR

    def enable(self):
        ''' Enables the class by finding the service and its characteristics. '''


        if self.ui_service is None:
            self.ui_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.led_char is None:
            self.led_char = self.ui_service.getCharacteristics(self.led_char_uuid)[0]
        if self.btn_char is None:
            self.btn_char = self.ui_service.getCharacteristics(self.btn_char_uuid)[0]
            self._ui_button_handle = self.btn_char.getHandle()
            self.btn_char_cccd = self.btn_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def set_led_mode_off(self):
        self.led_char.write(b"\x00", True)
        
    def set_led_mode_constant(self, r, g, b):
        teptep = "01{:02X}{:02X}{:02X}".format(r, g, b)
        self.led_char.write(binascii.a2b_hex(teptep), True)
        
    def set_led_mode_breathe(self, color, intensity, delay):
        '''
        Set LED to breathe mode.
        color has to be within 0x01 and 0x07
        intensity [%] has to be within 1-100
        delay [ms] has to be within 1 ms - 10 s
        '''
        teptep = "02{:02X}{:02X}{:02X}{:02X}".format(color, intensity,
                delay & 0xFF, delay >> 8)
        self.led_char.write(binascii.a2b_hex(teptep), True)
        
    def set_led_mode_one_shot(self, color, intensity):  
        '''
        Set LED to one shot mode.
        color has to be within 0x01 and 0x07
        intensity [%] has to be within 1-100
        '''
        teptep = "03{:02X}{:02X}".format(color, intensity)
        self.led_char.write(binascii.a2b_hex(teptep), True)

    def set_btn_notification(self, state):
        if self.btn_char_cccd is not None:
            if state == True:
                self.btn_char_cccd.write(b"\x01\x00", True)
            else:
                self.btn_char_cccd.write(b"\x00\x00", True)

    def disable(self):
        self.set_btn_notification(False)
        
    @property
    def ui_button_handle(self):
        return self._ui_button_handle
