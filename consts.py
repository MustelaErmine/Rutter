import os
import datetime

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def log(*args, sep=' '):
    dt = datetime.datetime.now()
    print(f'[{dt.strftime("%H:%M:%S %d %b %Y")}] {sep.join(str(arg) for arg in args)}')