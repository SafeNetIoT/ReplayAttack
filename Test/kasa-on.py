#!/usr/bin/env python3

#python3 kasa-onoff.py $name_plug $user_name $password $sleep_time_toswitch_plug_on

# Imports
from PyP100 import PyP110
import sys
import argparse
import time
from datetime import datetime
import subprocess
import os
import signal

"""
This script runs an experiment on the Tapo P110 Smart Plug.
It uses the https://github.com/fishbigger/TapoP100 library to control the plug.
"""

def get_ip(deviceid):

    """
    Function to return an IP address given a device name.
    It reads the devices.txt file and obtains the MAC address of the device.
    It then obtains the IP address after running an ARP query.

    Args:
        deviceid: Name of the device. This should correspond to the device identifier in the devices.txt file.
    Returns:
        ip_address: The IP address corresponding to the device.
    """

    # May change device file to user argument
    DEVICE_FILE = "/opt/moniotr/etc/devices.txt"
    ip_address = ""

    # Open file and read devices
    with open(DEVICE_FILE) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            mac = parts[0].strip()
            name = parts[1].strip()
            if name == deviceid:
                try:
                    arp = subprocess.Popen(["arp"], stdout=subprocess.PIPE)
                    out = subprocess.check_output(["grep", mac], stdin=arp.stdout)
                    ip_address = out.decode().split()[0].strip()
                except Exception as e:
                    print("Error running ARP:", e)

    return ip_address


def control_plug(plugid, username, password):

    # Get ip address of device
    ip_address = get_ip(plugid)
    if len(ip_address) == 0:
        sys.exit("IP address not found. Is your device present in the devices.txt file?")

    # Log into device
    try:
        print("Attempting connection to plug with device ID", plugid, "IP", ip_address)
        p110 = PyP110.P110(ip_address, username, password)
        p110.handshake()
        p110.login()
        info = p110.getDeviceInfo()
        name = p110.getDeviceName()
        print("Checking, device name:", name)
        print("Device info:", info)
    except Exception as e:
        print("Error in login to device:", e)
        sys.exit()

    p110.turnOn()


def main(program, args):

    # Create argument parser and arguments
    parser = argparse.ArgumentParser(prog=program, description="Run a Tapo P110 energy experiment.")
    parser.add_argument(
        "--plugid",
        type=str,
        help="Identifier of the plug.",
        default="testID"
    )
    parser.add_argument(
        "--username",
        type=str,
        help="Username to log into Tapo account.",
        default="test"
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password to log into Tapo account.",
        default="test"
    )

    # Parse arguments
    ns = parser.parse_args(args)

    # Run experiment
    control_plug(ns.plugid, ns.username, ns.password)

# Run!
if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
