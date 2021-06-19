from math import floor

ratio = 1.5


def scale(num):
    return floor(num * ratio)


def set_ratio(num):
    global ratio
    ratio = num
