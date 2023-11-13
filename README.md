```sudo python3 ./led.py 4B0084```
<hr />

```/sys/kernel/debug/hid``` Human Interface Devices \
```cat 0xxx\:048D\:C965.000x/rdesc``` \
```cat 0xxx\:048D\:C965.000x/events```
<hr />

Traceback (most recent call last): \
  File "/home/stellardeity/Documents/led-controller/./led.py", line 4, in <module> \
    from usb.backend.libusb1 import _Device \
ModuleNotFoundError: No module named 'usb' 

```sudo pip3 install pyusb```

