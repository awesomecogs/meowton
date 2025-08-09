import asyncio

import settings

from cat_detector import CatDetector
from feeder import Feeder
from util import Status

LED_PIN=4

class StatusLed():
    def __init__(self):

        if not settings.dev_mode:
            import pigpio
            self.__pigpio = pigpio.pi()
            self.__pigpio.set_mode(LED_PIN, pigpio.OUTPUT)


    async def task(self, feeder:Feeder, cat_detector:CatDetector):
        if settings.dev_mode:
            return
        import pigpio
        while True:
            if feeder.status==Status.OK and cat_detector.status==Status.OK:
                self.__pigpio.write(LED_PIN, pigpio.ON)
                await asyncio.sleep(1)
                self.__pigpio.write(LED_PIN, pigpio.OFF)
                await asyncio.sleep(0.1)
            else:
                self.__pigpio.write(LED_PIN, pigpio.ON)
                await asyncio.sleep(0.1)
                self.__pigpio.write(LED_PIN, pigpio.OFF)
                await asyncio.sleep(0.1)
