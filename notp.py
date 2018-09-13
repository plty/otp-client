#!/usr/bin/env python3
from time import time
from termcolor import colored
import sys
from pyotp import random_base32, TOTP
from collections import OrderedDict

users = OrderedDict()

users["dev:jrl"] = ("RRVB2WGWZK4UXHC6", "NuMoney-Dev", "jerrell@numoney.store")

cur_time = time()
time_left = 30 - int(cur_time % 30);

def token_print(secret, n):
    preferred_offset = 0 if time_left > 7 else 1
    for i in range(n):
        totp = TOTP(secret)
        token = totp.at(cur_time, i)
        token = token[:3] + '-' + token[3:6]
        if (i == preferred_offset):
            token = colored(token, "green")
        print(token)

def main(argv):
    print("Time Left:", time_left, "second(s)")
    for arg in argv:
        if users.get(arg) is not None:
            secret, site, username = users.get(arg)
            print(
                colored(arg, "blue"),
                ' ' * max(0, (8 - len(arg))) + '|',
                colored(site, 'yellow') + ':', colored(username, 'white'))
            token_print(secret, 2)
            print()
        else:
            print("otp not found")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main(users.keys())
