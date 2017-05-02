# coding=utf-8

import time
import random


def id_generate():
    part_date = str(time.time())[:10]
    part_random = str(random.random())[-6:]
    u_id = int(''.join([part_date, part_random]))
    return u_id

if __name__ == '__main__':
    print id_generate()
