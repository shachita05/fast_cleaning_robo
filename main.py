import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import random

# GPIO Pin Configuration
TRIG_PIN = 23
ECHO_PIN = 24
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 27
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 10
CLEANER_MOTOR = 5  # Optional motor for a cleaning brush

# MQTT Configuration
BROKER_ADDRESS = "your_mqtt_broker_address"
MQTT_TOPIC = "cleaning_robot/status"

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(CLEANER_MOTOR, GPIO.OUT)

# Initialize MQTT Client
client = mqtt.Client("CleaningRobot")
client.connect(BROKER_ADDRESS)

# Functions to Control Motors
def move_forward():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def move_backward():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)

def turn_left():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def turn_right():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def stop():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

# Start/Stop Cleaning Brush
def start_cleaning():
    GPIO.output(CLEANER_MOTOR, True)

def stop_cleaning():
    GPIO.output(CLEANER_MOTOR, False)

# Function to Measure Distance using Ultrasonic Sensor
def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    distance = round(distance, 2)
    return distance

# Main Cleaning Loop
try:
    start_cleaning()
    client.publish(MQTT_TOPIC, "Cleaning started")
    print("Cleaning started")

    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if distance < 20:
            # Obstacle detected, stop and choose a random turn
            stop()
            client.publish(MQTT_TOPIC, "Obstacle detected. Turning.")
            print("Obstacle detected. Turning.")
            time.sleep(1)

            # Randomly choose to turn left or right
            if random.choice([True, False]):
                turn_left()
                client.publish(MQTT_TOPIC, "Turning left")
                print("Turning left")
            else:
                turn_right()
                client.publish(MQTT_TOPIC, "Turning right")
                print("Turning right")
            time.sleep(1)
            
        else:
            # No obstacle, move forward
            move_forward()
            client.publish(MQTT_TOPIC, "Moving forward and cleaning")
            print("Moving forward and cleaning")
        
        time.sleep(0.1)  # Adjust the loop speed as needed

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    stop_cleaning()
    stop()
    GPIO.cleanup()
    client.disconnect()
