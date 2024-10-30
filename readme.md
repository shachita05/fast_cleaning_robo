---

# Simple Cleaning Robot

This project is for a basic autonomous cleaning robot that can move forward, detect obstacles, and avoid them using a Raspberry Pi, DC motors, and an ultrasonic sensor. It uses GPIO controls for motor movement and obstacle detection to enable the robot to navigate around its environment autonomously.

## Features

- **Obstacle Detection**: Uses an ultrasonic sensor to detect obstacles and avoid them by turning left or right.
- **Autonomous Navigation**: The robot moves forward and adjusts its direction when obstacles are detected.
- **Simple Logic**: Uses simple conditions to control movement, making it beginner-friendly.

## Requirements

### Hardware

- **Raspberry Pi** (any model with GPIO support)
- **Ultrasonic Sensor** (e.g., HC-SR04) for distance measurement
- **Two DC Motors** for movement
- **H-Bridge Motor Driver** (e.g., L298N) for controlling motor direction
- **Battery Pack** for powering the motors
- **Connecting Wires**

### Software

- **Raspbian OS** (or other Raspberry Pi compatible OS)
- **Python 3** with `RPi.GPIO` library installed

### Python Libraries

- `RPi.GPIO` for controlling GPIO pins on the Raspberry Pi

To install `RPi.GPIO`, run the following command on your Raspberry Pi:

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```

Or, if using `pip`:

```bash
pip install RPi.GPIO
```

## Installation

1. **Clone or download this repository** to your Raspberry Pi.
2. **Wire the hardware** according to the GPIO pin configuration in the code.
3. **Run the script**:

   ```bash
   python3 main.py
   ```

## Wiring Diagram

- **Ultrasonic Sensor**:
  - Trigger pin -> GPIO 23
  - Echo pin -> GPIO 24
- **Motors**:
  - Left Motor: GPIO 17 (forward), GPIO 27 (backward)
  - Right Motor: GPIO 22 (forward), GPIO 10 (backward)

## Code Explanation

- **Movement Functions**: Controls motor movement for `move_forward`, `stop`, `turn_left`, and `turn_right`.
- **Obstacle Detection**: Uses the ultrasonic sensor to measure the distance to nearby objects. If an obstacle is closer than 20 cm, the robot stops and turns in a random direction.
- **Main Loop**: The robot continuously moves forward and checks for obstacles. If an obstacle is detected, it stops, turns, and continues moving.

## Usage

1. Make sure the robot is in a clear area for testing.
2. Power on the Raspberry Pi and run the code.
3. The robot will move forward until it detects an obstacle, at which point it will stop, turn left or right, and resume moving.

## Troubleshooting

- **ModuleNotFoundError: No module named 'RPi'**: This error means the `RPi.GPIO` library is not installed. Install it on a Raspberry Pi using the instructions above.
- **Motors Not Responding**: Double-check your wiring and ensure the GPIO pins are correctly connected to the H-Bridge motor driver.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.

---

This `README.md` should help others understand the purpose, setup, and usage of your cleaning robot project!