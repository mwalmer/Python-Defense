from math import floor
import os
from ctypes import *

ratio = 1.5


def scale(num):
    return floor(num * ratio)


def set_ratio(num):
    global ratio
    ratio = num


def round_ratio(num):
    print("Ratio:", num)
    print("Scaled tile Px:", num * 32)
    print("Excess to be truncated:", (num * 32) % 2)
    print("Reduced to excess from ratio:", (((num * 32) % 2) / 32))
    print("Final rounded ratio:", num - (((num * 32) % 2) / 32))
    return num - (((num * 32) % 2) / 32)


def load_c_lib():
    path = os.path.join(os.path.dirname(__file__), "c_src.dll")
    lib = cdll.LoadLibrary(path)
    lib.modulo_zero.restype = c_bool
    lib.modulo_zero.argtypes = [c_int, c_int]
    lib.motion.restype = None
    lib.motion.argtypes = [c_double, c_double, c_void_p, c_void_p, c_double, c_double]
    lib.arc_motion.restype = None
    lib.arc_motion.argtypes = [c_double, c_double, c_void_p, c_void_p, c_double, c_double]
    lib.snake_shot.restype = None
    lib.snake_shot.argtypes = [c_double, c_double, c_void_p, c_void_p, c_double, c_double, c_double]
    lib.around_shot.restype = None
    lib.around_shot.argtypes = [c_void_p, c_void_p, c_double, c_double, c_int, c_double]
    return lib


# moved to here because load_c_lib function only needs to be run once
lib = load_c_lib()
