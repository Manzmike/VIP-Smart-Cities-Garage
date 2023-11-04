import time
import RPi.GPIO as GPIO

# -----------------------
# Define some functions
# -----------------------

def measure(pin):
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(pin)==0:
    start = time.time()

  while GPIO.input(pin)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average(pin):
  # This function takes 3 measurements and
  # returns the average.
  distance1=measure(pin)
  time.sleep(0.1)
  distance2=measure(pin)
  time.sleep(0.1)
  distance3=measure(pin)
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 21
GPIO_ECHO_TOP_LEFT    = 6
GPIO_ECHO_TOP_RIGHT    = 13
GPIO_ECHO_BOTTOM_LEFT    = 26
GPIO_ECHO_BOTTOM_RIGHT    = 19




print ("Ultrasonic Measurement")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_TOP_LEFT,GPIO.IN)      # Echo
GPIO.setup(GPIO_ECHO_TOP_RIGHT,GPIO.IN)      # Echo
GPIO.setup(GPIO_ECHO_BOTTOM_LEFT,GPIO.IN)      # Echo
GPIO.setup(GPIO_ECHO_BOTTOM_RIGHT,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:

  while True:

    distance = measure_average(GPIO_ECHO_TOP_LEFT)
    print('Top Left Distance : {:0.2f}'.format(distance))
    time.sleep(0.001)
    distance = measure_average(GPIO_ECHO_TOP_RIGHT)
    print('Top Right Distance : {:0.2f}'.format(distance))
    time.sleep(0.001)
    distance = measure_average(GPIO_ECHO_BOTTOM_LEFT)
    print('Bottom Left Distance : {:0.2f}'.format(distance))
    time.sleep(0.001)
    distance = measure_average(GPIO_ECHO_BOTTOM_RIGHT)
    print('Bottom Right Distance : {:0.2f}'.format(distance))
    time.sleep(0.001)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()

