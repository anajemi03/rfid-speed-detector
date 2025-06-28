import Jetson.GPIO as GPIO
import time
from serial import Serial

# Set GPIO pins for motor control
ENA = 33
IN1 = 35
IN2 = 37
ENB = 32
IN3 = 40
IN4 = 38

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup([ENA, IN1, IN2, ENB, IN3, IN4], GPIO.OUT)

# Initialize Serial Port for RFID
rfid_serial = Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# Function to send RFID command and read response
def send_rfid_cmd(cmd):
    data = bytes.fromhex(cmd)
    rfid_serial.write(data)
    response = rfid_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    return hex_space

# Set initial motor speed as a percentage of maximum speed
initial_speed_percent = 0.001  # Initial speed as a percentage (adjust as needed)

# Calculate PWM value based on percentage of maximum speed
initial_pwm_value = int(initial_speed_percent / 100.0 * 255)  # Assuming PWM range is 0-255

# Set initial motor speed using PWM value
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(ENB, GPIO.HIGH)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)
GPIO.output(ENA, GPIO.LOW)
GPIO.output(ENB, GPIO.LOW)
time.sleep(0.1 + initial_pwm_value / 255.0)

# Set default value for last_speed_percent
last_speed_percent = initial_speed_percent

try:
    while True:
        # Read RFID tag
        tag_data = send_rfid_cmd('BB 00 22 00 00 22 7E')
        # Convert RFID response to detected tag
        if '6C DC B9 33' in tag_data:  # Tag 1
            last_speed_percent = 3
            detected_tag = "Tag 1"
        elif '88 DD 43 D1' in tag_data:  # Tag 2
            last_speed_percent = 6
            detected_tag = "Tag 2"
        elif 'E8 DC 42 5E' in tag_data:  # Tag 3
            last_speed_percent = 0
            detected_tag = "Tag 3"
        else:
            detected_tag = "Unknown"
        
        # Print detected tag
        print("Detected Tag:", detected_tag)
        
        # Calculate PWM value based on percentage of maximum speed
        last_pwm_value = int(last_speed_percent / 100.0 * 255)  # Assuming PWM range is 0-255
        
        # Set the motor speed
        if last_speed_percent > 0:
            # Set ENA and ENB to HIGH for forward direction
            GPIO.output(ENA, GPIO.HIGH)
            GPIO.output(ENB, GPIO.HIGH)
            # Adjust speed by changing the duty cycle of ENA and ENB
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            time.sleep(0.1)
            # Change duty cycle based on the last detected speed
            GPIO.output(ENA, GPIO.LOW)
            GPIO.output(ENB, GPIO.LOW)
            time.sleep(0.1 + last_pwm_value / 255.0)
        else:
            # Stop the motors if speed is 0
            GPIO.output(ENA, GPIO.LOW)
            GPIO.output(ENB, GPIO.LOW)

except KeyboardInterrupt:
    # Clean up GPIO pins when the program stops
    GPIO.cleanup()
