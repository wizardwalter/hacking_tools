#!/usr/bin/env python3
import subprocess
import sys


def set_monitor_mode(enable=True):
    if enable:
        print("Enabling monitor mode...")
        subprocess.run(["sudo", "airmon-ng", "check", "kill"])
        subprocess.run(["sudo", "airmon-ng", "start", "wlan0"])
    else:
        print("Disabling monitor mode and restoring normal Wi-Fi...")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"])
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["on", "off"]:
        print("Usage: python3 monitor_mode.py [on|off]")
        sys.exit(1)

    enable_monitor = sys.argv[1] == "on"
    set_monitor_mode(enable_monitor)


if __name__ == "__main__":
    main()
