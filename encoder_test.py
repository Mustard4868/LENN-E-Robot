from machine import I2C, Pin
import time

# Define I2C pins
i2c_mplex = I2C(scl=Pin(22), sda=Pin(21))

# Address of I2C multiplexer
MULTIPLEXER_ADDR = 0x70

# Address of AS5600 sensor
AS5600_ADDR = 0x36

# Configuration registers
REG_MAGNET = 0x0
REG_ANGLE = 0x0E

# Function to select I2C channel on the multiplexer
def select_channel(channel):
    i2c_mplex.writeto(MULTIPLEXER_ADDR, bytes([1 << channel]))

# Function to read angle from AS5600 sensor
def read_angle():
    angle_data = i2c.readfrom_mem(AS5600_ADDR, REG_ANGLE, 2)
    angle = (angle_data[0] << 8 | angle_data[1]) & 0x0FFF
    return angle

# Main loop
while True:
    # Select the appropriate channel on the multiplexer
    select_channel(0)  # Assuming AS5600 sensor is connected to channel 0 of the multiplexer
    
    angle = read_angle()
    print("Angle: ", angle)
    time.sleep(1)  # Wait for 1 second
