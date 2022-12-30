This file is a documentation of the pirover project

### List of Hardware components
*  Raspberry pi Zero W ![Raspberry pi zero w 50] (https://cdn.shopify.com/s/files/1/0176/3274/products/raspberry-pi-zero-w-raspberry-pi-sc0020-14879106433086_700x.jpg?v=1646233385)
* RaspiRobot V3f ![RaspiRobot V3f] (https://cdn-shop.adafruit.com/970x728/1940-00.jpg)
* LIPO 18650 3.7V ![Meco 18650](https://imgaz3.staticbg.com/thumb/large/upload/2015/08/SKU243560f.jpg.webp)
* Motors and Wheels and Frame ![robot car]( https://imgaz.staticbg.com/images/oaupload/banggood/images/52/5D/9592fa14-feb1-4f27-8620-c019798f1faf.JPG.webp)
* Servo Mounting unit ![acrylic mounting unit] (https://imgaz.staticbg.com/images/oaupload/banggood/images/D4/4E/9a72eaba-dc09-4fdf-bdbd-9c72458607fb.jpg.webp)
* SG90 Servos x 3 ![SG90](https://imgaz.staticbg.com/images/oaupload/banggood/images/8A/71/ad565f44-2f37-4234-9257-2335f840f41c.jpg.webp)
* VL53L0X Time of Flight sensor ![time-of-flight](https://makershop.ie/image/cache/catalog/p/00380/YXB087-3-1000x1000.jpg.webp)
* 18650 3x batter holder ![battery holder](https://makershop.ie/image/cache/catalog/p/00319/YXK657-1-1000x1000h.jpg.webp)
* Pan&tilt mechanism ![pan&tilt](https://media.digikey.com/Photos/Sparkfun%20Elec%20%20Photos/MFG_ROB-14391_View-1.jpg)
* tiny breadboard ![small breadboard](https://ae01.alicdn.com/kf/Ha92919baa95d4107b1d8dca59a5a8bb4B.jpg)
* nylon standoff and screw ![nylong standoff](https://m.media-amazon.com/images/I/71DlhH3C6gL._SL1500_.jpg)
* brass standoffs ![brass standoff](https://m.media-amazon.com/images/I/71glvdYevdL._AC_SL1500_.jpg)
* nightvision camera ![pinightvision](https://cdn.shopify.com/s/files/1/0176/3274/products/camera-board-for-raspberry-pi-night-vision-5mp-waveshare-wav-10300-30241841676483_700x.jpg?v=1646620562)
* proximity sensor x2 ![proximity](https://m.media-amazon.com/images/I/61htb9cKSqL._SL1500_.jpg)
* jst connectors ![jst connectors](https://m.media-amazon.com/images/I/51gvmKC9iKS._AC_SL1001_.jpg)
* jumperwires ![jumperwires](https://m.media-amazon.com/images/I/71d0rjq6xDL._SL1001_.jpg)
* Magnifying glass with lamp ![magnifying glass](https://ie.farnell.com/productimages/standard/en_GB/2769999-40.jpg)
* Helping hand
* nylon ties ![nylon ties](https://m.media-amazon.com/images/I/71ovecKeEKL._AC_SL1500_.jpg)

### Python
The python code has been taken from the followng libraries
1. Simon Monks python library [rrb3](https://github.com/simonmonk/raspirobotboard3)
2. Hands-On MQTT programming with Python by  by [Gaston C. Hillar](https://learning.oreilly.com/library/view/hands-on-mqtt-programming/9781789138542/)
3. Building a streaming library with [picamera]( http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming )

### Node-Red
Node-red was used to develop an interface for controlling the car and camera. It was also used as a means of being able to see the streaming video of the rover

### MQTT
Finally, I wanted to use MQTT to pass messages to the rover and get telemetry data from the rover. 

### Hardware considerations

#### Using the time of flight sensor (VL53L0X)
Initially I tried the traditional HC-SR04. However the drawback with this was that it ultrsound is not the best wave to bounce off fabric. So Couches and curtans were not detected very well.

I had to add the proximity sensor to overcome when theultrasonic sensor was not very good at this. This added further logic to the code.

The time-of-flight sensors have become quite cheap. The one that I am using does not have a big range. However because the rover is not going at speed anywhere it was easy to incorporate the VL53L0X into the design.

I might be able to remove the proximity sensor once I am have been able to code the time-of-flight sensor better.

I am using pimoroni's [VL53L0X](https://github.com/pimoroni/VL53L0X-python) library.

I am using 3 of the 18650 batteries, although one should have been sufficient. This allows me to play a little longer.

#### Servos (SG90)
I have not had much success with controlling the jitter on the servos.
I used a variety of libraris to experiment with controlling the jitter.
My idea of electricity and PWM is very basic. So the controls for the camera servos ae not very good.

![top](../images/pirover_top.jpeg)
![front](../images/pirover_front.jpeg)

#### Node-red mobile interface
![node-red](../images/node-red_interface.jpeg)
