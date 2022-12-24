from rover import Rover
from time import sleep
import logging
import logging.config
import yaml

with open('logging.conf.yaml', 'r') as f:
	config = yaml.safe_load(f.read())
	logging.config.dictConfig(config)

logger = logging.getLogger('my_logger')

bot = Rover(12, 6)
bot.set_servo_mid()

try:
	while True:
		bot.forward(speed=0.6)
		distance = bot.tof_get_distance()
		logger.debug("distance: " + str(distance))
		if distance < 20:
			logger.info("distance is less than 20")
			bot.stop()
			bot.turn()
		if bot.check_stuck(distance):
			logger.info("stuck")
			bot.reverse(1, 0.5)
			bot.turn()
 
		#if bot.obstacle():
		#	logger.info("stuck or hit obstacle")
		#	bot.reverse(1, 0.5)
		#	bot.turn()
		sleep(0.2)
finally:
	logger.info("cleaning up")
	bot.cleanup()
