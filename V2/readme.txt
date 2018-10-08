Robotito



**google & stackoverflow are your friends**


	* 3D parts were designed in Blender to fit 8 sensors, 4 motors and encoders, a camera, a Raspberry Pi 3, and Adafruit Motor Shield, yet still maintain as much of the original Robotito design as 	possible.

	* Blender files use .blend format. Those were then exported to .stl files to 3D print them. 

	* Files to 3D print for the Robotito are found in the RobotitoParts folder

		Camera Back 					x 1
		Camera Front 					x 1
		Miniwheels 					x 64
		WheelTotal(This file contains 2 wheels)		x 2
		SensorHolderTotal				x 1
		RobotitoChassis 				x 1

	* Parts to order are in \robotito-master\V2\PartsToOrder.xlsx

	* The motors chosen were 6v with 1.2 stall amps. They have a gearbox reducing the RPM to ~500RPM. This should provide plenty of torque to accelerate the robot, and plenty of speed to move the 	robot quickly. The motors have hall sensor encoders to give precise feedback of the rotation of each wheel to aid in positioning.


********************************************ROBOTITO BUILD*******************************************************

	CHASSIS
	* Attach hub to wheel with two screws, across from each other
	* Insert axle into miniwheels and place in wheel back with hub
	* Attach front of wheel to hub. (Screw in two remaining open holes in wheel)
	* Insert motors into motor brackets
	* Attach motors/brackets to chassis (Ensure the wires from the encoder are passing upwards through the holes in the chassis)
	* Attach 3" spacers to chassis 

	* Place camera in camera enclosure and screw on front. (Holes may need to be cleaned out with a drill)

	WIRING (**FIRST** Test all components via breadboard to ensure they work properly)
	* Solder provided female headers to BOTTOM of Adafruit Motor Driver Servo Hat(AMD)
	* Solder motor wire mounts to the TOP of the AMD
	* Solder 13 pin male headers to TOP of AMD in GND, 3V, and 5V
	* Solder male header pins to TOP of AMD for additional Pi inputs(at least for CE0, MOSI, MISO, and SCLK)
	* Place 16 pin socket on BOTTOM of board prototyping area, with 5 pads to the left and 6 pads to the right of it. Bend the pins inward so they are touching the pad directly above or below it.
	* Solder MCP3008 socket pins as well as the pads next to them that they are bent towards to create connection points for the wires.
	* Solder a group of header wires(the female end) to each pad next to a pin
	(The dotted side of the chip will be facing left when holding the board with the motor pins facing downwards)
	* Test for continuity, and make sure there aren't any accidentally bridged solder pads
	* Crimp a male pin to the Vcc on all sensors, and female pins on the remaining wires
	* Connect all the wires to the appropriate pins
	* Pass camera cable through the hole on the AMD and connect to Pi camera port
	* Plug AMD into Raspberry Pi
	* Screw in 1/2 inch spacers in between AMD and Pi
	* Screw in 1 inch spacers to remaining 2 holes on pi
	* Screw in to sensor holder
	* Pass sensors through holes in sensor holder
	* Screw in sensors to sensor holder
	* Screw camera into chassis
	* Screw in 3 inch spacers to chassis and sensor holder
	* Celebrate because you have completed your mission to build a robotito
	* Lament because now you have to do the programming(Just kidding it's really not that bad)

     	* Download Raspbian Linux
	download  here https://www.raspberrypi.org/downloads/raspbian/
	(Download via torrent, if you value your time)
	The .iso will need to go on a SD card of at least 8GB. 

	* To login in remotely, enable SSH before you boot. Create a file called ssh(no file format!!) in the boot partition (the only partition that's normally visible to Windows and Mac computers). The 	ssh file does not have to contain anything, it's presence tells Raspbian you want SSH enabled and the file will be deleted after that's done. 
	
	User name: pi
	Password: raspberry
	(Change pw ASAP)

    	* Update
		sudo apt-get update
     	* Get python-dev
		sudo apt-get install python-dev python-pip
		pip install upgrade distribute
		pip install upgrade rpi.gpio
     	* Install Adafruit Motor-HAT-Python Library
		https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
     	* Install Adafruit MCP3008 Library
		sudo apt-get update
		sudo apt-get install build-essential python-dev python-smbus git
		cd ~
		git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
		cd Adafruit_Python_MCP3008

		sudo python setup.py install
		sudo apt-get update
		sudo apt-get install build-essential python-dev python-smbus python-pip
		sudo pip install adafruit-mcp3008


    	* Turn on camera, spi and i2c
		sudo raspi-config (in interfacing options, and turn each one on)
		(using lsmod, you should see spi_bcm2835, i2c_bcm2835)
     	* Install Raspbian on Pi

CRAZYFLIE
     * Install dependencies 
     	Ros (lunar)
     	crazyflie-ROS 
     	cfclient
     
     	git clone https://github.com/bitcraze/crazyflie-client-python
     	git clone https://github.com/whoenig/crazyflie_ros.git
     	
     	dependencies for controllers(you will need xbox and wi controllers)
     	
     	follow the setup instructions here (beginning on pg. 4)
     	http://act.usc.edu/publications/Hoenig_Springer_ROS2017.pdf
     	
     * Every time a new instance of catkin workspace is made, make sure you type
     	source/devel/setup.bash
     
     

	
