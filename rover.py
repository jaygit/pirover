
# rrb3.py Library

import RPi.GPIO as GPIO
import time

import logging
import logging.config
import yaml
import VL53L0X

with open('logging.conf.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('my_logger')

class RRB3:

    MOTOR_DELAY = 0.2

    RIGHT_PWM_PIN = 14
    RIGHT_1_PIN = 10
    RIGHT_2_PIN = 25
    LEFT_PWM_PIN = 24
    LEFT_1_PIN = 17
    LEFT_2_PIN = 4
    SW1_PIN = 11
    SW2_PIN = 9
    LED1_PIN = 8
    LED2_PIN = 7
    OC1_PIN = 22
    OC2_PIN = 27
    OC2_PIN_R1 = 21
    OC2_PIN_R2 = 27
    TRIGGER_PIN = 18
    ECHO_PIN = 23
    left_pwm = 0
    right_pwm = 0
    pwm_scale = 0

    old_left_dir = -1
    old_right_dir = -1

    def __init__(self, battery_voltage=9.0, motor_voltage=6.0, revision=2):

        logger.info("RRB3:__init__")
        self.pwm_scale = float(motor_voltage) / float(battery_voltage)

        if self.pwm_scale > 1:
            print("WARNING: Motor voltage is higher than battery votage. Motor may run slow.")

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.LEFT_PWM_PIN, GPIO.OUT)
        self.left_pwm = GPIO.PWM(self.LEFT_PWM_PIN, 500)
        self.left_pwm.start(0)
        GPIO.setup(self.LEFT_1_PIN, GPIO.OUT)
        GPIO.setup(self.LEFT_2_PIN, GPIO.OUT)

        GPIO.setup(self.RIGHT_PWM_PIN, GPIO.OUT)
        self.right_pwm = GPIO.PWM(self.RIGHT_PWM_PIN, 500)
        self.right_pwm.start(0)
        GPIO.setup(self.RIGHT_1_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_2_PIN, GPIO.OUT)

        GPIO.setup(self.LED1_PIN, GPIO.OUT)
        GPIO.setup(self.LED2_PIN, GPIO.OUT)

        GPIO.setup(self.OC1_PIN, GPIO.OUT)
        if revision == 1:
            self.OC2_PIN = self.OC2_PIN_R1
        else:
            self.OC2_PIN = self.OC2_PIN_R2

        GPIO.setup(self.OC2_PIN_R2, GPIO.OUT)

        GPIO.setup(self.SW1_PIN, GPIO.IN)
        GPIO.setup(self.SW2_PIN, GPIO.IN)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
        logger.info("RRB3:set_motors")
        if self.old_left_dir != left_dir or self.old_right_dir != right_dir:
            self.set_driver_pins(0, 0, 0, 0)    # stop motors between sudden changes of direction
            time.sleep(self.MOTOR_DELAY)
        self.set_driver_pins(left_pwm, left_dir, right_pwm, right_dir)
        self.old_left_dir = left_dir
        self.old_right_dir = right_dir

    def set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):
        logger.info("RRB3:set_driver_pins")
        self.left_pwm.ChangeDutyCycle(left_pwm * 100 * self.pwm_scale)
        GPIO.output(self.LEFT_1_PIN, left_dir)
        GPIO.output(self.LEFT_2_PIN, not left_dir)
        self.right_pwm.ChangeDutyCycle(right_pwm * 100 * self.pwm_scale)
        GPIO.output(self.RIGHT_1_PIN, right_dir)
        GPIO.output(self.RIGHT_2_PIN, not right_dir)

    def forward(self, seconds=0, speed=1.0):
        logger.info("RRB3:forward")
        self.set_motors(speed, 0, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        logger.info("RRB3:stop")
        self.set_motors(0, 0, 0, 0)

    def reverse(self, seconds=0, speed=1.0):
        logger.info("RRB3:reverse")
        self.set_motors(speed, 1, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def left(self, seconds=0, speed=0.5):
        logger.info("RRB3:left")
        self.set_motors(speed, 0, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def right(self, seconds=0, speed=0.5):
        logger.info("RRB3:right")
        self.set_motors(speed, 1, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def step_forward(self, delay, num_steps):
        logger.info("RRB3:step_forward")
        for i in range(0, num_steps):
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

    def step_reverse(self, delay, num_steps):
        logger.info("RRB3:step_reverse")
        for i in range(0, num_steps):
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

    def sw1_closed(self):
        logger.info("RRB3:sw1_closed")
        return not GPIO.input(self.SW1_PIN)

    def sw2_closed(self):
        logger.info("RRB3:sw2_closed")
        return not GPIO.input(self.SW2_PIN)

    def set_led1(self, state):
        logger.info("RRB3:set_led1")
        GPIO.output(self.LED1_PIN, state)

    def set_led2(self, state):
        logger.info("RRB3:set_led2")
        GPIO.output(self.LED2_PIN, state)

    def set_oc1(self, state):
        logger.info("RRB3:set_oc1")
        GPIO.output(self.OC1_PIN, state)

    def set_oc2(self, state):
        logger.info("RRB3:set_oc2")
        GPIO.output(self.OC2_PIN, state)

    def _send_trigger_pulse(self):
        logger.info("RRB3:_send_trigger_pulse")
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.0001)
        GPIO.output(self.TRIGGER_PIN, False)

    def _wait_for_echo(self, value, timeout):
        logger.info("RRB3:_wait_for_echo")
        count = timeout
        while GPIO.input(self.ECHO_PIN) != value and count > 0:
            count -= 1

    def get_distance(self):
        logger.info("RRB3:get_distance")
        self._send_trigger_pulse()
        self._wait_for_echo(True, 10000)
        start = time.time()
        self._wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm

    def cleanup(self):
        logger.info("RRB3:cleanup")
        GPIO.cleanup()

class Rover(RRB3):
    MOTOR_DEFAULT = 0.5
    TURN_TIME = 0.2
    TURN_SPEED = 0.3
    
    RANGE_PWM_PIN = 21
    RANGE_MAX = 180
    RANGE_MIN = 0
    PAN_PWM_PIN = 20
    PAN_MAX = 160
    PAN_MIN = 0
    TILT_PWM_PIN = 16
    TILT_MAX = 160
    TILT_MIN = 20
    STEP = 10
    IR_PIN_LEFT = 26 
    IR_PIN_RIGHT = 19
    TOF_I2C_ADDRESS = 0x29
    

    def __init__(self, battery_voltage=9.0, motor_voltage=6.0):
        logger.info("Rover:__init__")

        self.pan_current = 0
        self.tilt_current = 0
        self.range_current =0
        self.tof_timing = 20000
        self.distance_readings = [0, 0, 0, 0, 0]
        self.tof_distance_reading = [0, 0, 0, 0, 0]
        super().__init__(battery_voltage, motor_voltage)

        # time of flight sensor
        self.tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
        self.tof.open() # initialise it.
        self.tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        GPIO.setup(self.RANGE_PWM_PIN, GPIO.OUT)
        self.range_pwm = GPIO.PWM(self.RANGE_PWM_PIN, 50)
        self.range_pwm.start(0)

        GPIO.setup(self.PAN_PWM_PIN, GPIO.OUT)
        self.pan_pwm = GPIO.PWM(self.PAN_PWM_PIN, 50)
        self.pan_pwm.start(0)

        GPIO.setup(self.TILT_PWM_PIN, GPIO.OUT)
        self.tilt_pwm = GPIO.PWM(self.TILT_PWM_PIN, 50)
        self.tilt_pwm.start(0)
        
        GPIO.setup(self.IR_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IR_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.set_servo_mid()


    def servo_angle(self, servo, angle):
        logger.info("Rover:servo_angle")
        if servo == "pan":
            self.set_pan_angle(angle)
        elif servo == "tilt":
            self.set_tilt_angle(angle)
        elif servo == "range":
            self.set_range_angle(angle)
            

    
    def set_servo_mid(self):
        logger.info("Rover:set_servo_mid")
        self.set_pan_angle(90)
        self.set_tilt_angle(90)
        self.set_range_angle(90)

    def __correct_range__(self,angle):
        logger.info("Rover:__correct_range__")
        if angle > self.RANGE_MAX:
            angle = self.RANGE_MAX
        elif angle < self.RANGE_MIN:
            angle = self.RANGE_MIN
        return(angle)

    def __correct_pan__(self,angle):
        logger.info("Rover:__correct_pan__")
        if angle > self.PAN_MAX:
            angle = self.PAN_MAX
        elif angle < self.PAN_MIN:
            angle = self.PAN_MIN
        return(angle)

    def __correct_tilt__(self,angle):
        logger.info("Rover:__correct_tilt__")
        if angle > self.TILT_MAX:
            angle = self.TILT_MAX
        elif angle < self.TILT_MIN:
            angle = self.TILT_MIN
        return(angle)

    def pan_left(self):
        logger.info("Rover:pan_left")
        angle = self.pan_current + self.STEP
        self.set_pan_angle(angle)

    def pan_right(self):
        logger.info("Rover:pan_right")
        angle = self.pan_current - self.STEP
        self.set_pan_angle(angle)

    def tilt_up(self):
        logger.info("Rover:tilt_up")
        angle = self.tilt_current - self.STEP
        self.set_tilt_angle(angle)

    def tilt_down(self):
        logger.info("Rover:servo_down")
        angle = self.tilt_current + self.STEP
        self.set_tilt_angle(angle)

    def set_pan_angle(self, angle):
        logger.info("Rover:set_pan_angle")
        angle = self.__correct_pan__(angle)
        self.pan_current = angle
        pwm_cycle = 2 + (angle/18)
        self.pan_pwm.ChangeDutyCycle(pwm_cycle)
        time.sleep(self.MOTOR_DELAY)
        self.pan_pwm.ChangeDutyCycle(0)

    def set_tilt_angle(self, angle):
        logger.info("Rover:set_tilt_angle")
        angle = self.__correct_tilt__(angle)
        self.tilt_current = angle
        pwm_cycle = 2 + (angle/18)
        self.tilt_pwm.ChangeDutyCycle(pwm_cycle)
        time.sleep(self.MOTOR_DELAY)
        self.tilt_pwm.ChangeDutyCycle(0)

    def set_range_angle(self, angle):
        logger.info("Rover:set_range_angle")
        angle = self.__correct_range__(angle)
        self.range_current = angle
        pwm_cycle = 2 + (angle/18)
        self.range_pwm.ChangeDutyCycle(pwm_cycle)
        time.sleep(self.MOTOR_DELAY)
        self.range_pwm.ChangeDutyCycle(0)


    def tof_get_distance(self):
        """Use the time of flight to calculate
           distance
        Param: None
        return: int-> the distance from obstacle in cms
        """
        logger.info("Rover:tof_get_distance")
        distance = self.tof.get_distance()
        time.sleep(self.tof_timing/100000.00)
        logger.debug(f"TOF Distance: {distance/10}")
        return (distance/10)

    def get_direction(self):
        logger.info("Rover:get_direction")
        self.set_range_angle(30)
        # distance_right = self.get_distance()
        tof_distance_right = self.tof_get_distance()
        self.set_range_angle(90)
        time.sleep(self.MOTOR_DELAY)
        self.set_range_angle(150)
        # distance_left = self.get_distance()
        tof_distance_left = self.tof_get_distance()
        self.set_range_angle(90)
        # if (max(distance_left, distance_right) > 20 and max(tof_distance_left, tof_distance_right) > 20) or not self.obstacle():
        if (max(tof_distance_left, tof_distance_right) > 20) or not self.obstacle():
            if tof_distance_left > tof_distance_right:
                return("left")
            else:
                return("right")
        else:
            return("reverse")

    def turn(self, time=0.5, speed=0.5):
        logger.info("Rover:turn")
        direction = self.get_direction()
        if direction == "left":
            self.left(time, speed)
        elif direction == "right":    
            self.right(time, speed)
            check_direction = self.get_direction()
        elif direction == "reverse":
            self.reverse(time, speed)
            self.turn()
        distance = self.get_distance()
        if distance < 20:
            self.turn()
        self.stop()

    def check_stuck(self, distance):
        logger.info("Rover:check_stuck")
        self.distance_readings = self.distance_readings[1:]
        self.distance_readings.append(distance)
        if max(self.distance_readings) - min(self.distance_readings) > 3:
            return False
        return True

    def check_proximity_left(self):
        """ Check the left proximity sensor """
        if GPIO.input(self.IR_PIN_LEFT) == False:
            return True
        return False
 
    def check_proximity_right(self):
        """ Check the right proximity sensor """
        if GPIO.input(self.IR_PIN_RIGHT) == False:
            return True
        return False
 
    def obstacle(self):
        logger.info("Rover:obstacle")
        if GPIO.input(self.IR_PIN_LEFT) == False  or GPIO.input(self.IR_PIN_RIGHT) == False:
            return True
        else:
            return False
    
    def cleanup(self):
        logger.info("Rover:cleanup")
        self.range_pwm.stop()
        self.pan_pwm.stop()
        self.tilt_pwm.stop()
        self.tof.stop_ranging()
        self.tof.close()
        GPIO.cleanup()
