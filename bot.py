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
		distance = bot.get_distance()
		logger.info("distance: " + str(distance))
		bot.forward(speed=0.6)
		if distance < 20:
			logger.info("distance is less than 20")
			bot.stop()
			bot.turn()
		if bot.check_stuck(distance) or bot.obstacle():
			logger.info("stuck or hit obstacle")
			bot.reverse(1, 0.5)
			bot.turn()
		sleep(0.2)
finally:
	logger.info("cleaning up")
	bot.cleanup()
