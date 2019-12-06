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
from bluepy.btle import Peripheral,ADDR_TYPE_RANDOM

from .battery import BatterySensor
from .environment import EnvironmentService
from .ui import UserInterfaceService
from .motion import MotionService
from .sound import SoundService
from .delegate import ThingyDelegate

    
class Thingy52(Peripheral):
    '''
    Thingy:52 module. Instance the class and enable to get access to the Thingy:52 Sensors.
    The addr of your device has to be know, or can be found by using the hcitool command line 
    tool, for example. Call "> sudo hcitool lescan" and your Thingy's address should show up.
    '''
    def __init__(self, addr,delegate=None):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)

        self.battery = BatterySensor(self)
        self.environment = EnvironmentService(self)
        self.ui = UserInterfaceService(self)
        self.motion = MotionService(self)
        self.sound = SoundService(self)
        if delegate is not None:
            self.setDelegate(delegate)
