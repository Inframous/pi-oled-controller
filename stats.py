import re
import time
import subprocess
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import psutil
from datetime import datetime

# Define the Reset Pin for the OLED display
oled_reset = digitalio.DigitalInOut(board.D4)

# Set up the OLED screen size
WIDTH = 128
HEIGHT = 64
BORDER = 2
FONT_SIZE = 11

# Use I2C for communication
i2c = board.I2C()  # uses board.SCL and board.SDA
disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear the display
disp.fill(0)
disp.show()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Load a smaller monospaced font to ensure consistency
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
font_size = FONT_SIZE
font = ImageFont.truetype(font_path, font_size)

# Draw a progress bar
def draw_progress_bar(draw, x, y, width, height, progress, max_value=100):
    bar_width = int(progress / max_value * width)
    draw.rectangle((x, y, x + bar_width, y + height), outline=255, fill=255)
    draw.rectangle((x + bar_width, y, x + width, y + height), outline=255, fill=0)

# Get system stats
def get_ip():
    ip = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode().strip()
    return "IP: " + ip

def get_cpu():
    return psutil.cpu_percent()

def get_mem():
    mem = psutil.virtual_memory()
    return mem.used / (1024 ** 3), mem.total / (1024 ** 3)  # in GB

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage.percent

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime = f"{uptime_seconds / 3600:.2f}"
    return uptime.split(".")

# Vertical spacing for each line
num_lines = 5  # Number of lines to display information (IP, CPU, Mem, Disk, Uptime)
line_height = (HEIGHT - BORDER * 2) // num_lines  # Divide screen into equal parts for each line
print("Starting oled display...")
FIRST_LOOP = True
try:
    while True:
        # Draw a black filled box to clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Get system information
        cpu = get_cpu()
        mem_used, mem_total = get_mem()
        disk = get_disk_usage()
        ip = get_ip()
        uptime = get_uptime()

        # Starting Y position for the first row of text
        top = BORDER

        # Draw IP Address
        draw.text((0, top), ip, font=font, fill=255)
        top += line_height

        # Draw CPU usage label (no progress bar now)
        draw.text((0, top), "CPU: %.1f%%" % cpu, font=font, fill=255)
        top += line_height

        # Draw Memory usage in GB (no progress bar)
        draw.text((0, top), "Mem: %.1fGB/%.1fGB" % (mem_used, mem_total), font=font, fill=255)
        top += line_height

        # Draw Disk usage label and progress bar
        draw.text((0, top), "Disk: %.1f%%" % disk, font=font, fill=255)
        draw_progress_bar(draw, 70, top + 2, width - 72, 8, disk)  # Progress bar starting at x=70
        top += line_height

        # Toggle between displaying Uptime and current time
        current_time = datetime.now().strftime("%H:%M:%S")
        if int(time.time()) % 10 < 5:
            # Show current time (live, updates every second)
            draw.text((0, top), f"Time: {current_time}", font=font, fill=255)
        else:
            # Show uptime (doesn't change every second, updates every 5 seconds)
            draw.text((0, top), f"Uptime: {uptime[0]}h {uptime[1]}m", font=font, fill=255)

        # Display the image
        disp.image(image)
        disp.show()

        # Wait for the next cycle (1 second for real-time updates)
        if FIRST_LOOP == True:
            FIRST_LOOP = False
            print("Oled display activated.")
        time.sleep(1)

except KeyboardInterrupt:
    disp.fill(0)
    disp.show()
    exit()
