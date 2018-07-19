"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="localhost", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    while True:
        client.send_message("/head", 1/100*-1)
        for x in range(100):
            client.send_message("/head", (1-x/100)*-1)
            print(1-x/100)
            time.sleep(0.05)
        for x in range(100):
            client.send_message("/head", x/100)
            time.sleep(0.05)
        for x in range(100):
            client.send_message("/head", 1-x/100)
            time.sleep(0.05)
        for x in range(100):
            client.send_message("/head", (x/100)*-1)
            time.sleep(0.05)
