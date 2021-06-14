ratio = 1.5


def scale(num):
    return int(num / 32 * (32 * ratio))


def set_ratio(num):
    global ratio
    ratio = num
