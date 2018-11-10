#!/usr/bin/env python3
import sys
from collections import OrderedDict
from termcolor import colored
from time import time
from pyotp import random_base32, TOTP
from pyperclip import copy

users = OrderedDict()
users["dev:jrl"] = ("RRVB2WGWZK4UXHC6", "some-website", "john@example.com")

cur_time = time()
time_left = 30 - int(cur_time % 30);

def token_print(secret, n):
    preferred_offset = 0 if time_left > 7 else 1
    for i in range(n):
        totp = TOTP(secret)
        token = totp.at(cur_time, i)
        token_formatted = token[:3] + '-' + token[3:]
        if (i == preferred_offset):
            token_formatted = colored(token_formatted, "green")
            try: 
                copy(token)
            except Exception as e:
                pass
        print(token_formatted)

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
