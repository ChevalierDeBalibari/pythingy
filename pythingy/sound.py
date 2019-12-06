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
from .static import write_uint8

from .uuid import SOUND_SERVICE_UUID
from .uuid import S_CONFIG_CHAR_UUID
from .uuid import S_SPEAKER_DATA_CHAR_UUID
from .uuid import S_SPEAKER_STATUS_CHAR_UUID
from .uuid import S_MICROPHONE_CHAR_UUID
from .uuid import CCCD_UUID

import binascii

class SoundService():
    '''
    Sound service module. Instance the class and enable to get access to the Sound interface.
    '''
    serviceUUID                 = Nordic_UUID(SOUND_SERVICE_UUID)
    config_char_uuid            = Nordic_UUID(S_CONFIG_CHAR_UUID)
    speaker_data_char_uuid      = Nordic_UUID(S_SPEAKER_DATA_CHAR_UUID)
    speaker_status_char_uuid    = Nordic_UUID(S_SPEAKER_STATUS_CHAR_UUID)
    microphone_char_uuid        = Nordic_UUID(S_MICROPHONE_CHAR_UUID)

    def __init__(self, periph):
        self.periph = periph
        self.sound_service = None
        self.config_char = None
        self.speaker_data_char = None
        self.speaker_status_char = None
        self.speaker_status_char_cccd = None
        self.microphone_char = None
        self.microphone_char_cccd = None
        self._s_microphone_handle = None
        self._s_speaker_status_handle = None

    def enable(self):
        ''' Enables the class by finding the service and its characteristics. '''
        if self.sound_service is None:
            self.sound_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.config_char is None:
            self.config_char = self.sound_service.getCharacteristics(self.config_char_uuid)[0]
        if self.speaker_data_char is None:
            self.speaker_data_char = self.sound_service.getCharacteristics(self.speaker_data_char_uuid)[0]
        if self.speaker_status_char is None:
            self.speaker_status_char = self.sound_service.getCharacteristics(self.speaker_status_char_uuid)[0]
            self._s_speaker_status_handle = self.speaker_status_char.getHandle()
            self.speaker_status_char_cccd = self.speaker_status_char.getDescriptors(forUUID=CCCD_UUID)[0]
        if self.microphone_char is None:
            self.microphone_char = self.sound_service.getCharacteristics(self.microphone_char_uuid)[0]
            self._s_microphone_handle = self.microphone_char.getHandle()
            self.microphone_char_cccd = self.microphone_char.getDescriptors(forUUID=CCCD_UUID)[0]

    def play_speaker_sample(self, sample=0):
        if self.speaker_data_char is not None:
            sample_str = "{:02X}".format(sample)
            self.speaker_data_char.write(binascii.a2b_hex(sample_str), False)

    def set_speaker_status_notification(self, state):
        if self.speaker_status_char_cccd is not None:
            if state == True:
                self.speaker_status_char_cccd.write(b"\x01\x00", True)
            else:
                self.speaker_status_char_cccd.write(b"\x00\x00", True)

    def set_microphone_notification(self, state):
        if self.microphone_char_cccd is not None:
            if state == True:
                self.microphone_char_cccd.write(b"\x01\x00", True)
            else:
                self.microphone_char_cccd.write(b"\x00\x00", True)

    def configure(self, speaker_mode=None, microphone_mode=None):
        if speaker_mode is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, speaker_mode, 0)
            self.config_char.write(binascii.a2b_hex(new_config), True)
        if microphone_mode is not None and self.config_char is not None:
            current_config = binascii.b2a_hex(self.config_char.read())
            new_config = write_uint8(current_config, microphone_mode, 1)
            self.config_char.write(binascii.a2b_hex(new_config), True)

    def disable(self):
        self.set_speaker_status_notification(False)
        self.set_microphone_notification(False)
        
    @property
    def s_speaker_status_handle(self):
        return self._s_speaker_status_handle
    
    @property
    def s_microphone_handle(self):
        return self._s_microphone_handle
    
