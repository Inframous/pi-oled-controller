# Ras-Pi Oled Display Controller

## Overview
The **Ras-Pi Oled Display Controller** is a project designed to control and display information on an OLED screen connected to a Raspberry Pi. The project allows you to monitor and display various system statistics, including uptime, CPU usage, memory usage, and custom messages on a small, energy-efficient OLED screen.

## Features
- Displays real-time system statistics
    - CPU usage
    - Memory usage 
    - Disk Usage
    - Time/Uptime

- Supports custom message display.
- Can be modified to show different information.
- Compatible with the Pi52 OLED displays on Raspberry Pi (e.g., using I2C interface).

## Requirements
- **Hardware:**
  - Raspberry Pi (any model with I2C support)
  - OLED Display (typically 0.91" or similar, I2C interface)

- **Software:**
  - Raspberry Pi OS (or any Linux-based OS for Raspberry Pi)
  - Python 3
  - Libraries: `Adafruit_SSD1306`, `psutil`, `RPi.GPIO` (for GPIO pins)

## Installation (Standard)

### 1. Clone the Repository
Clone the repository to your Raspberry Pi and run the files using python:

```bash
git clone https://github.com/yourusername/ras-pi-oled-display-controller.git
cd ras-pi-oled-display-controller
python3 main.py
```

## Installation (Docker)
Clone the repository to your Raspberry Pi and run the docker compose file:
```bash
git clone https://github.com/yourusername/ras-pi-oled-display-controller.git
cd ras-pi-oled-display-controller
sudo docker compose up -d
```

Note: Make sure you've enabled the I2C and SPI interfaces under `raspi-config`.
