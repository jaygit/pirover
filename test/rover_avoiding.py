# Attach: SR-04 Range finder, switch on SW1, and of course motors.

# The switch SW2 stops and starts the robot

from rrb3 import *
import time, random
import pickle
import sys, socket
import csmodule as cs
from envirophat import light, motion, weather, leds, analog

BATTERY_VOLTS = 6 
MOTOR_VOLTS = 6

HOST = cs.HOST 
PORT = cs.PORT
distance_readings = [0, 0, 0, 0, 0]
motion_readings = []
last_z = 0

out = open('enviro.log', 'w')
out.write('light\trgb\tmotion\theading\ttemp\tpress\n')

rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)

# client program to communicate with raspicam for turning servos
def check_motion():
    global motion_readings, last_z
    threshold = 0.01
    motion_readings.append(motion.accelerometer().z)
    motion_readings = motion_readings[-4:]
    z = sum(motion_readings) / len(motion_readings)
    print(abs(z -last_z))
    if last_z > 0 and abs(z -last_z) > threshold:
	print("returning True in check_motion")
        return True
    last_z = z
    return False
    
def check_obstacle_sensor():
    if int(analog.read(0)) == 0:
        return True 
    return False 

def check_stuck(distance):
    global distance_readings
    distance_readings = distance_readings[1:]
    distance_readings.append(distance)
    if max(distance_readings) - min(distance_readings) > 3:
        return False 
    return True
    
def check_distance(angle):
	msg = "close"
	try:
		sock = socket.socket(socket.AF_INET,
					socket.SOCK_STREAM)
		sock.connect((HOST,PORT))
		print('\nConnected to {}:{}'.format(HOST, PORT))
		msg = pickle.dumps({"object": "servo", "number": 1, "angle": angle})
		cs.send_msg(sock, msg)  #Blcoks until sent
		print("Sent Message")
		msg = cs.recv_msg(sock) # Block until
						# received complete
						# message
		print('Received echo: ' + msg)
	except socket.error as e:
		print('Socket error {}'.format(e))
		return msg
	finally:
		sock.close()
		print('Closed connection to server\n')

        distance = rr.get_distance()
        if distance > 40 and not check_obstacle_sensor():
		msg = "ok"
	return msg

# if you dont have a switch, change the value below to True
running = True
def turn_randomly():
    turn_time = 1
    if random.randint(1, 2) == 1:
	if "ok" in check_distance(110):
		rr.left(turn_time, 0.5) # turn at half speed
    else:
	if check_distance(30) == "ok":
		rr.right(turn_time, 0.5)
    check_distance(70)
    rr.stop()
    #capture_environ()

def capture_environ():
	distance = rr.get_distance()
	lux = light.light()
	leds.on()
	rgb = str(light.rgb())[1:-1].replace(' ', '')
	leds.off()
	acc = str(motion.accelerometer())[1:-1].replace(' ', '')
	heading = motion.heading()
	temp= weather.temperature()
	press = weather.pressure()
	out.write('%f\t%s\t%s\t%f\t%f\t%f\n' % (lux, rgb, acc, heading, temp, press))
	print('%f\t%s\t%s\t%f\t%f\g%f\n' % (lux, rgb, acc, heading, temp, press))

	
try:
    check_distance(70)
    while True:
        distance = rr.get_distance()
	#while distance > 1400:
	#	print(distance)
	print(distance)
        if (distance < 20 or check_obstacle_sensor()) and running:
            turn_randomly()
        if running:
            # if (not check_motion()) or check_stuck(distance):
            if check_stuck(distance):
                rr.reverse(1, 0.5)
                turn_randomly()
            rr.forward(0, 0.5)
        #if rr.sw2_closed():
        #    running = not running
        if not running:
            rr.stop()
        time.sleep(0.2)
finally:
    print("Exiting")
    rr.cleanup()
    
