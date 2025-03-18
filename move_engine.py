#!/usr/bin/env python
"""Basic blinking led example.

The led on A20-OLinuXino-MICRO blinks with a heartbeat-like rate.
"""

import os
import sys
import time
import asyncio

from main import steps_per_revolution

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from pyA20.gpio import gpio
from pyA20.gpio import port

__author__ = "Stefan Mavrodiev"
__copyright__ = "Copyright 2014, Olimex LTD"
__credits__ = ["Stefan Mavrodiev"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "support@olimex.com"


def millis():
    return time.time() * 1000

# Налаштовуємо GPIO-піни
DIR = port.PA6   # GPIO2 - Напрямок
STEP = port.PA11  # GPIO10 - Імпульси
EN = port.PA12    # GPIO2

gpio.init()
gpio.setcfg(DIR, gpio.OUTPUT)
gpio.setcfg(STEP, gpio.OUTPUT)
gpio.setcfg(EN, gpio.OUTPUT)


async def step(min):
    """
    Асинхронна функція для керування кроками двигуна.
    Блокуючі виклики time.sleep() замінено на await asyncio.sleep().
    """
    steps = int(min * (steps_per_revolution/60))
    try:
        if steps > 0:
            gpio.output(DIR, 1)
            for _ in range(int(steps)):
                gpio.output(STEP, 1)
                await asyncio.sleep(0.01)  # асинхронна затримка
                gpio.output(STEP, 0)
                await asyncio.sleep(0.01)
        elif steps < 0:
            gpio.output(DIR, 0)
            for _ in range(int(abs(steps))):
                gpio.output(STEP, 1)
                await asyncio.sleep(0.01)
                gpio.output(STEP, 0)
                await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        print("Operation cancelled.")
        raise
    except Exception as e:
        print("An error occurred:", e)

