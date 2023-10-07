import platform
import sys
from enum import Enum

class Platform(Enum):
    UNKNOWN = 0
    WIN = 1
    LINUX = 2
    MAC = 3


def print_details():
    print('Platform:\t{}'.format(platform.platform()))
    print('Platform (sys):\t{}'.format(sys.platform))
    print('Machine:\t{}'.format(platform.machine()))


def get_platform() -> Platform:
    if sys.platform.lower().startswith('win32') != -1:
        return Platform.WIN
    elif platform.platform().lower().find('linux') != -1:
        return Platform.LINUX
    elif platform.platform().lower().find('darwin') != -1:
        return Platform.MAC # Not tested with Apple silicon
    else:
        raise Exception('Unknown platform')
