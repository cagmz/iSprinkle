#!/bin/bash
printf "Updating list of packages...\n\n"
sudo apt-get update
printf "Updating packages, firmware, and kernel...\n\n"
sudo apt-get -y dist-upgrade
