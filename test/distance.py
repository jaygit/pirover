from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
from gpiozero import AngularServo


from gpiozero import DistanceSensor
from time import sleep


#Device.pin_factory = PiGPIOFactory()
#servo = AngularServo(6)
#servo.angle = 60
while True:
	sensor = DistanceSensor(echo=8, trigger=7)
	print('Distance: ', sensor.distance * 100)
#	servo.angle= 10
#	sleep(1)
#	servo.angle= 40
#	sleep(1)
#	servo.angle= 60
#	sleep(1)
#	servo.angle= -60
	sleep(1)


	
