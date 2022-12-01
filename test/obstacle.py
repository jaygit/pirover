from rover import Rover
from time import sleep

bot = Rover(12, 6)

while True:
	if bot.obstacle():
		print("Near")
	else:
		print("not detected")
	sleep(1)
