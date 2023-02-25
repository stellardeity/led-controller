#!/usr/bin/env python

from collections.abc import Generator
from usb.backend.libusb1 import _Device
import usb.core
import re

device_type = type(Generator[_Device, None, None] | None)

class LedController:
    def __init__(self):
        device: device_type = usb.core.find(idVendor=0x048D, idProduct=0xC965)
        if device is None:
            raise ValueError("Light device not found")

        # [Errno 16] Resource busy
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        self.device = device

    def build_control_string(
            self,
            effect,
        ):
        data = [204, 22]

        if effect == "off":
            data.append(1)
            data += [0] * 30
            return data

        data += [1, 1, 2]
        
        chunk: list[int] = []
        effect = effect.lower()
        if re.match(r"^[0-9a-f]{6}$", effect):
            chunk = [
                int(effect[i : i + 2], 16) for i in range(0, len(effect), 2)
            ]
        else:
            raise ValueError(f"Invalid effect format: {effect}")

        data += chunk*4
        data += [0] * 15
        return data

    def send_control_string(self, data):
        self.device.ctrl_transfer(
            bmRequestType=0x21,
            bRequest=0x9,
            wValue=0x03CC,
            wIndex=0x00,
            data_or_wLength=data,
        )

if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser(
        description="Lenovo Legion 5 Pro 2023 keyboard light controller"
    )

    argparser.add_argument("effect", nargs="+", help="{off, hex}")

    args = argparser.parse_args()

    controller = LedController()
    data = controller.build_control_string(
        effect=args.effect[0],
    )

    controller.send_control_string(data)

# Alatfar is the brightest star in my sky
