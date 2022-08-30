Dependencies:

To sucessefully get solution for satellite ephemeris and time, this script requires installation of following libraries:


Georinex(required):
	This is a parsing library which reads the RINEX file. Install this to your python environment through any package manager, I use pip.
	
	To install, go to your terminal and use the following command,
	
	pip install georinex 
	

Manim CE (optional to make animations ):
	To run the animation, you have to install manimCE in your system.
	
	I have included two scripts that installs manim on mac and linux system.
	
	You have to change permissions first:
	
	Go to this directory in terminal and do the following:
	
	chomd +x mac.sh
	
	or 
	
	chmod +x linux.sh
	
	and after that execute the script as follows:
	
	./mac.sh
	
	or 
	./linux.sh
	
	
	If it doesn't work, follow instructions on this link
	
	Please  refer to folloing link:
	https://docs.manim.community/en/stable/installation.html
	
	Installation depens on your OS.



Usuag:

Just solution:
	If you just want solutions without animation, you can run solution.py script just to get solution for position and time.  
	Note: It writes the solution to a text file. 


Solution with animation:
	If you want both solution and animation, use animate_orbit.py script. Running this won't get you animation. You have to follow manim syntax to render animations.
	
	Open current directory (where run_animation.sh is located) in terminal after manim installation, and use the following command:
	
	first do the followng(only required first time):
	
	chmod +x run_animation.sh
	
	then do to get animation:
	
	./run_animation.sh
		
	
------------ Video information ---------------------------------	
	
	Runtime: 4 min
	
	The video rendered will be saved under media directory in the current directory
	
	The solution.txt will be saved in your current working director. You dont have to run solution.py again. This does it's job automatically.	


