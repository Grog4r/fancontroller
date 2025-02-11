import RPi.GPIO as GPIO
import time

# GPIO setup
FAN_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_GPIO, GPIO.OUT)

# Temperature thresholds (in degrees Celsius)
TEMP_ON = 60  # Turn fan on at this temperature
TEMP_OFF = 50  # Turn fan off below this temperature


def get_cpu_temperature():
    """Read the CPU temperature from the system."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.readline()
    return int(temp) / 1000.0  # Convert millidegree Celsius to Celsius


def control_fan():
    """Control the fan based on CPU temperature."""
    fan_on = False
    try:
        while True:
            cpu_temp = get_cpu_temperature()
            print(f"CPU temperature is {cpu_temp}°C")
            if cpu_temp >= TEMP_ON and not fan_on:
                GPIO.output(FAN_GPIO, GPIO.HIGH)
                fan_on = True
                print("Fan ON!")
            elif cpu_temp <= TEMP_OFF and fan_on:
                GPIO.output(FAN_GPIO, GPIO.LOW)
                fan_on = False
                print("Fan OFF!")
            time.sleep(5)  # Check temperature every 5 seconds
    except KeyboardInterrupt:
        print("Fan control stopped by user.")
    finally:
        GPIO.output(FAN_GPIO, GPIO.LOW)  # Turn off the fan
        GPIO.cleanup()


if __name__ == "__main__":
    control_fan()
